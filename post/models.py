# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	text = models.CharField(max_length = 200,default = 'nai')
	# image = models.FileField( upload_filed = '', width='', height='', null = True, blank = True )		//https://www.youtube.com/watch?v=Rr1-UTFCuH4  upload image properly
	image = models.FileField(null = True, blank = True )
	type = models.CharField(max_length = 40, blank = True, null = True)
	by_id = models.ForeignKey(User, blank = True, null = True, related_name="owner")
	time = models.DateTimeField(blank = True, null = True)
	visibility_by_admin =  models.BooleanField(default=True)

	def __str__(self):
   			return "{} at {}".format(self.by_id, self.time)



class Post_comments(models.Model):
	value = models.TextField(blank = True, null = True)
	time = models.DateTimeField(blank = True, null = True)
	by_id = models.ForeignKey(User, blank = True, null = True, related_name="owner+")
	of_post_id = models.ForeignKey("Post", null = False, default = '1', related_name="comment of post +")
	visibility_by_admin =  models.BooleanField(default=True)


class Post_like(models.Model):
	value =  models.BooleanField(default=True)
	time = models.DateTimeField(blank = True, null = True)
	by_id = models.ForeignKey(User, blank = True, null = True, related_name="owner+")
	of_post_id = models.ForeignKey("Post",null = False, default = '1', related_name="like of post +")


class Post_images(models.Model):
	size = models.IntegerField()
	of_post_id =  models.ForeignKey("Post", null = False, default = '1', related_name="books")
	# path = models.CharField(max_length=1000)
