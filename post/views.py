# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render
from django.views.generic import DetailView
from django.shortcuts import redirect, HttpResponseRedirect
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
		print(ThisPostId)
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
				history_object.delete()	

			elif current_value == False:	#current value down
				history_object.value = 1
				history_object.save()		# update to up

		else:			# don't have history  
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
				history_object.delete()	

			elif current_value == True:	#current value up
				history_object.value = 0
				history_object.save()		# downgrade to down

		else:			# don't have history  
			post_like.save()	# insert up
 

	else:
		form = InsertPost

	post = Post.objects.all()
	context = {
		'post':post,
		'form':form,
	}
	return render(request, 'index.html',context)

class SinglePost(DetailView):
	model = Post
	template_name = "single_post.html"


	def post(self,request,*args,**kwargs):
		post_comments = Post_comments()
		post_like = Post_like()
		self.object = self.get_object()
		context = context = super(SinglePost, self).get_context_data(**kwargs)
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

				if current_value == True:		#current value up
					history_object.delete()	

				elif current_value == False:	#current value down
					history_object.value = 1
					history_object.save()		# update to up

			else:			# don't have history  
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
					history_object.delete()	

				elif current_value == True:	#current value up
					history_object.value = 0
					history_object.save()		# downgrade to down

			else:			# don't have history  
				post_like.save()	# insert up


		return self.render_to_response(context=context)