# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.shortcuts import redirect
from .forms import RegistrationForm,UserLoginForm
# Create your views here.

def enter(request):
	title = 'enter'
	context = {
		"title": title,
	}
	return render(request, "enter.html",context)

##################
def logInRegisterUser(request):
	###################login##################
	loginForm = UserLoginForm(request.POST or None)
	if loginForm.is_valid() and 'log-in' in request.POST:
		print('log-in')
		username = loginForm.cleaned_data.get("username")
		password = loginForm.cleaned_data.get("password")
		user = authenticate(username = username, password = password)
		# if not user or not user.check_password(password):
		# 	raise validation error
		login(request, user)
		return redirect('/')
		# print(request.user.is_authenticated())
	
	###################registration###################
	registrationForm = RegistrationForm(request.POST or None)
	if registrationForm.is_valid() and 'sign-up' in request.POST:
		user2 = registrationForm.save(commit = False)
		password2 = registrationForm.cleaned_data.get('password')
		user2.set_password(password2)
		user2.save()
		new_user = authenticate(username = user2.username, password = password2)
		login(request, new_user)
	###################errors###################
	
	###################errors###################
	# url page
	context = {
		"loginForm":loginForm,
		"registrationForm":registrationForm,
		"re":request.POST,
	
	}

	###################return###################
	return render(request,"enter.html",context)


def is_auth(request):
	if request.user.is_authenticated:
		return true 
	else:
		return false
# def registerStudent(request):
# 	form = RegistrationForm(request.POST or None)
# 	if form.is_valid():
# 		user = form.save(commit = False)
# 		password = form.cleaned_data.get('password')
# 		user.set_password(password)
# 		user.save()

# 		new_user = authenticate(username = user.username, password = password)
# 		login(request, new_user)

# 	context = {
# 		"form":form,
# 		"title1":"Register",
# 	}
# 	return render(request, 'enter.html',context)