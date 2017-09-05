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

	puthere = 'agei nai kicu';
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