	# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render
from django.views.generic import DetailView
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post, Post_like,Post_comments
from .forms import InsertPost
# Create your views here.


@login_required
def main_page(request):
	post = Post()
	post_like = Post_like()

	if request.method == 'POST' and 'insert_post' in request.POST:
		form = InsertPost(request.POST or None, request.FILES or None)
		if form.is_valid():
			post.text = form.cleaned_data['text']
			post.image = form.cleaned_data['image']
			post.type="post"
			post.time = datetime.datetime.now()
			post.by_id = request.user
			post.save()


	elif request.method == 'POST' and 'delete_post' in request.POST:
		form = InsertPost
		ThisPostId = request.POST['delete_post']
		# print(ThisPostId)
		ThisPost = Post.objects.filter(id=ThisPostId)
		ThisPost.delete()


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
				if (post.post_down != 0 or post.post_down > 0 ):
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
 

	else:
		form = InsertPost

	post = Post.objects.all()
	post_like = Post_like.objects.all()
	ThisUser = request.user.id
	ThisUserLike = Post_like.objects.filter(by_id = ThisUser)

	context = {
		'post':post,
		'form':form,
		'post_like':post_like,
		'ThisUserLike':ThisUserLike,
		'null':0,
	}
	return render(request, 'index.html',context)



class SinglePost(DetailView):
	model = Post
	template_name = "single_post.html"


	def post(self,request,*args,**kwargs):
		post_comments = Post_comments()
		post_like = Post_like()
		self.object = self.get_object()

		if request.method == 'POST' and 'delete_single_post' in request.POST:	#delete_post
			ThisPostId = request.POST['delete_single_post']
			ThisPost = Post.objects.filter(id=ThisPostId)
			ThisPost.delete()
			return HttpResponseRedirect('../../')
		elif request.method == 'POST' and 'submit_comment' in request.POST:	#comments
			post_comments.value = request.POST['comment']
			post_comments.time = datetime.datetime.now()
			post_comments.visibility_by_admin = 1
			post_comments.by_id =  request.user
			post_comments.of_post_id = Post.objects.get(id=request.POST['post_id'])
			post_comments.save()
		elif request.method == 'POST' and 'up' in request.POST:		#clicked up
			post_like.value = 1
			post_like.time = datetime.datetime.now()
			post_like.by_id =  request.user
			post_like.of_post_id = Post.objects.get(id=request.POST['post_like_id'])
			history = Post_like.objects.filter(by_id = post_like.by_id , of_post_id = post_like.of_post_id)

			if history:		# have history
				history_object = Post_like.objects.get(by_id = post_like.by_id , of_post_id = post_like.of_post_id)
				current_value = history_object.value
				print()
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

		context = self.get_context_data()
		return self.render_to_response(context=context)

	def get_context_data(self, **kwargs):
		post_like = Post_like()
		post_comments = Post_comments()
		post = Post.objects.all()
		context = super(SinglePost, self).get_context_data(**kwargs)
		ThisPostId = self.kwargs['pk']
		ThisPost = Post.objects.get(id=ThisPostId)

		ThisPostLike = Post_like.objects.filter(of_post_id = ThisPostId)
		ThisPostTotalUp  = 0
		ThisPostTotalDown  = 0
		for ThisPostLike in ThisPostLike:
			if ThisPostLike.value == True:
				ThisPostTotalUp= ThisPostTotalUp+ 1
			elif ThisPostLike.value == False:
				ThisPostTotalDown = ThisPostTotalDown + 1
		LikeByRequestedUser = Post_like.objects.filter(by_id = self.request.user.id , of_post_id = ThisPostId)
		for LikeByRequestedUser in LikeByRequestedUser:
			LikeByRequestedUser = LikeByRequestedUser.value
		ThisPostComments = Post_comments.objects.filter(of_post_id = ThisPostId)
		ThisPostCommentsNumber = 0
		for obj in ThisPostComments:
			# ThisPostCommentsNumber = ThisPostCommentsNumber + 1 ;
			# obj+ = 1
			ThisPostCommentsNumber += 1 ;

		#update like/unlike
		

		# ThisUser.id = User.objects.get(id = 1)

		ThisUser = User.objects.all()

		context = {
			'post': ThisPost,
			'ThisUser': ThisUser,
			'ThisPostComments': ThisPostComments,
			'ThisPostTotalUp': ThisPostTotalUp,
			'ThisPostTotalDown': ThisPostTotalDown,
			'LikeByRequestedUser': LikeByRequestedUser,
			'ThisPostCommentsNumber':ThisPostCommentsNumber,

		}
		return context





