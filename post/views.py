# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render

from .models import Post
from .forms import InsertPost
# Create your views here.


@login_required
def main_page(request):
	post = Post()
	if request.method == 'POST':
		form = InsertPost(request.POST or None, request.FILES or None)
		if form.is_valid():
			post.text = form.cleaned_data['text']
			post.image = form.cleaned_data['image']
			post.type="post"
			post.time = datetime.datetime.now()
			post.by_id = request.user
			post.save()
	else:
		form  = InsertPost

	post = Post.objects.all()
	context = {
		'post':post,
		'form':form,
	}
	return render(request, 'index.html',context)
