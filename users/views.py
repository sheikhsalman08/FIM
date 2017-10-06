# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from .social_auth_settings import settingss,password
from social_django.models import UserSocialAuth

from social_core.pipeline.user import USER_FIELDS, get_username as social_get_username, create_user, user_details
from random import randrange
import datetime

from post.models import Post,Post_like,Post_comments
from django.views.generic import DetailView
from post.forms import InsertPost

# Create your views here.

def registerStudent(request):
	print(request.user.is_authenticated())
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit = False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)

	context = {
		"form":form,
		"hi":"user",
	}
	return render(request, 'form.html',context)

@login_required
def delete_account(request):
	user = request.user
	user_id = request.user.id
	user_is_staff = request.user.is_staff

	if request.POST and user_is_staff==0:	#if not superuser or staff
		# user.update(favorite_food="ramen")
		user_d = User.objects.get(id = user_id)
		user_d.is_active = 0
		user_d.save()
		logout(request)
		pot = "submitted"
		return HttpResponseRedirect('../enter')
	else:
		pot = "not submitted"


	context = {
		"pot": pot
	}
	return render(request,'delete_account.html',context)	

@login_required
def update_settings(request):

	if request.method == 'POST':
		print(request.method)
		user_id = request.user.id
		user_d = User.objects.get(id = user_id)
		user_d.first_name = request.POST['firstName']
		user_d.last_name = request.POST['lastName']
		user_d.email = request.POST['email']
		user_d.save()
		user_id = request.user.id

	user_id = request.user.id

	if request.user.email:
		email = request.user.email
	else:
		email = "-----"
	
	user = request.user

	try:
		github_login = user.social_auth.get(provider='github')
	except UserSocialAuth.DoesNotExist:
		github_login = None

   	try:
		facebook_login = user.social_auth.get(provider='facebook')
	except UserSocialAuth.DoesNotExist:
		facebook_login = None

	can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

	###############################

	puthere = '-';
	if request.method == 'GET' and 'value' in request.method:
		puthere = request.GET['value']
		print(request.GET['value'])
	else:
		puthere = '';

	###############################
	context = {
			"user_id":request.user.id,
			"user_first_name":request.user.first_name,
			"user_last_name":request.user.last_name,
			"user_email": email,
			'github_login': github_login,
	        'facebook_login': facebook_login,
	        'can_disconnect': can_disconnect,
	        "puthere": puthere,
		}	

	return render(request,'settings.html',context)

@login_required
def update_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
        redirect_here = '../enter'
    else:
        PasswordForm = AdminPasswordChangeForm
        redirect_here = '../enter'

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(redirect_here)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    context = {
    	'form':form,
    }
    return render(request, 'password.html', context)

class User_profile(DetailView):
	model = User
	template_name = "user.html"
	
	def post(self,request,*args,**kwargs):
		post = Post()
		post_like = Post_like()
		self.object = self.get_object()
		form = InsertPost(self.request.POST or None, self.request.FILES or None)
		context = self.get_context_data()
		if request.method == 'POST' and 'insert_post' in request.POST:

			if form.is_valid():
				self.object = self.get_object()
				context = context = super(User_profile, self).get_context_data(**kwargs)
				post.text = form.cleaned_data['text']
				post.image = form.cleaned_data['image']
				post.type="post"
				post.time = datetime.datetime.now()
				post.by_id = self.request.user
				post.save()

				profile_user_id = self.kwargs['pk']
				
				context['form']=InsertPost 

				user_post = Post.objects.filter(by_id_id = profile_user_id)
				context['user_post']=user_post			

			else:
				self.object = self.get_object()
				context = context = super(User_profile, self).get_context_data(**kwargs)
				form = InsertPost

				profile_user_id = self.kwargs['pk']

				context['form']=form 

				user_post = Post.objects.filter(by_id_id = profile_user_id)
				context['user_post']=user_post			

		elif request.method == 'POST' and 'delete_post' in request.POST:
				self.object = self.get_object()
				context = context = super(User_profile, self).get_context_data(**kwargs)
				form = InsertPost
				ThisPostId = request.POST['delete_post']
				ThisPost = Post.objects.filter(id=ThisPostId)
				ThisPost.delete()
				context['form']=form 

				profile_user_id = self.kwargs['pk']
				user_post = Post.objects.filter(by_id_id = profile_user_id)
				context['user_post']=user_post			

				return self.render_to_response(context=context)
		elif request.method == 'POST' and 'submit_comment' in request.POST:
			post_comments.value = request.POST['comment']
			post_comments.time = datetime.datetime.now()
			post_comments.visibility_by_admin = 1
			post_comments.by_id =  request.user
			post_comments.of_post_id = post.objects.get(id=request.POST['post_id'])
			post_comments.save()



		elif request.method == 'POST' and 'up' in request.POST:		#clicked up
			form = InsertPost
			post_like.value = 1
			post_like.time = datetime.datetime.now()
			post_like.by_id =  request.user
			post_like.of_post_id = Post.objects.get(id=request.POST['post_like_id'])
			history = Post_like.objects.filter(by_id = post_like.by_id , of_post_id = post_like.of_post_id)

			if history:		# have history
				history_object = Post_like.objects.get(by_id = post_like.by_id , of_post_id = post_like.of_post_id)
				current_value = history_object.value

				if current_value == True:		#current value up
					post = Post.objects.get(id=request.POST['post_like_id'])
					if (post.post_up != 0 or post.post_up > 0 ):
						post.post_up = post.post_up - 1					
						post.save()

					history_object.delete()	

				elif current_value == False:	#current value down
					post = Post.objects.get(id=request.POST['post_like_id'])
					post.post_up = post.post_up + 1
					if (post.post_down != 0 or post.post_down > 0):
						post.post_down = post.post_down - 1
					post.save()

					history_object.value = 1
					history_object.save()		# update to up

			else:			# don't have history  
				post = Post.objects.get(id=request.POST['post_like_id'])
				post.post_up = post.post_up + 1
				post.save()
				
				post_like.save()	# insert up


		elif request.method == 'POST' and 'down' in request.POST:		#clicked down
			form = InsertPost
			post_like.value = 0
			post_like.time = datetime.datetime.now()
			post_like.by_id =  request.user
			post_like.of_post_id = Post.objects.get(id=request.POST['post_like_id'])
			history = Post_like.objects.filter(by_id = post_like.by_id , of_post_id = post_like.of_post_id)

			if history:		# have history
				history_object = Post_like.objects.get(by_id = post_like.by_id , of_post_id = post_like.of_post_id)
				current_value = history_object.value

				if current_value == False:		#current value down

					post = Post.objects.get(id=request.POST['post_like_id'])
					if (post.post_down != 0 or post.post_down > 0 ):
						post.post_down = post.post_down - 1					
						post.save()

					history_object.delete()	

				elif current_value == True:	#current value up
					post = Post.objects.get(id=request.POST['post_like_id'])
					if (post.post_up != 0 or post.post_up > 0):
						post.post_up = post.post_up - 1
					post.post_down = post.post_down + 1
					post.save()
					
					history_object.value = 0
					history_object.save()		# downgrade to down

			else:			# don't have history  
				post = Post.objects.get(id=request.POST['post_like_id'])
				post.post_down = post.post_down + 1
				post.save()

				post_like.save()	# insert up
		return self.render_to_response(context=context)



	def get_context_data(self, **kwargs):
		context = super(User_profile, self).get_context_data(**kwargs)
		profile_user_id = self.kwargs['pk']
		user_post = Post.objects.filter(by_id_id = profile_user_id)
		form = InsertPost(self.request.POST or None, self.request.FILES or None)
		profile_user_id = self.kwargs['pk']
		ThisUser= User.objects.filter(id = profile_user_id)
		ThisUser.id = User.objects.get(id = profile_user_id) #can't use without .id at the end as it's already use as filter now when using wiht get use as a instance of that

		post_like = Post_like.objects.all()
		ThisUser2 = self.request.user.id
		ThisUserLike = Post_like.objects.filter(by_id = ThisUser2)

		context = {
			'user_post': user_post,
			'form':form,
			'ThisUser': ThisUser,
			'ThisUser.id':ThisUser.id,

			'post_like':post_like,
			'ThisUserLike':ThisUserLike,
			'null':0,			
		}
		return context


def get_username(strategy, details, user=None, *args, **kwargs):		###to social auth user
    result = social_get_username(strategy, details, user=user, *args, **kwargs)
    # result['username'] = '-'.join([
    #     result['username'],strategy, str(randrange(0, 1000))
    # ])
    result['username'] = '-'.join([
        details['username'],str(randrange(0, 1000))
    ])
    print(details)
	
    return result