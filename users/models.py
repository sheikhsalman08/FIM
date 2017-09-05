# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
# class User(models.Model):
# 	name = models.CharField(max_length = 50)
# 	choices = (
# 				(u'1',u'administrator'),
# 				(u'2',u'member'),
# 			  )
# 	type = models.CharField(max_length = 1, choices = choices)
# 	own_img = models.FileField(null = True, blank = True)			#https://www.youtube.com/watch?v=Rr1-UTFCuH4
# 	institute_id = models.IntegerField(blank = True, null = True , default = 0)
# 	email = models.TextField(blank = True, null = True)
# 	contact_number = models.TextField(blank = True, null = True)
# 	birth_year = models.IntegerField(blank = True, null = True , default = 0)
# 	choices = (
# 				(u'0',u'unverified'),
# 				(u'1',u'verified'),
# 			  )
# 	verification = models.IntegerField(choices = choices)
# 	username = models.CharField(max_length = 10)
# 	choices = (
# 				(u'0', u'hide'),
# 				(u'1', u'Show'),
# 			  )
# 	visibility_by_admin = models.CharField(max_length = 1, choices = choices)

class UserProfile(models.Model):		#https://www.youtube.com/watch?v=qLRxkStiaUg&t=232s	 
	user = models.OneToOneField(User)
	institute_id = models.IntegerField(blank = True, null = True , default = 1)
	contact_number = models.CharField(blank = True, null = True,max_length=12)
	verification = models.BooleanField()
	show_name = models.CharField(max_length = 10)
	choices = (
				(u'1',u'administrator'),
				(u'2',u'member'),
		  	  )
	type = models.CharField(max_length = 1, choices = choices)



# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
# import os

# def get_image_path(instance, filename):
#     return os.path.join('photos', str(instance.id), filename)

# class UserProfile(models.Model):
#     user = models.ForeignKey(User, unique=True)
#     profile_image = ImageField(upload_to=get_image_path, blank=True, null=True)
# 	# own_img = models.ImageField.path = os.path.join('/Upload/image', generated_image_path)
# 	# own_img = models.ImageField.path = os.path.join('/Upload/image')

