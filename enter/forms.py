from django.http import HttpResponse,request
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserLoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		user_active = User.objects.filter(username = username)
		for x in user_active:
			print(x.is_active)
			if not x.is_active:
				raise forms.ValidationError("This user is no longer active")

		if username and password:
			# user = authenticate(request,username = username, password = password,**kwargs)
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Log in Failed")

		# if not user.check_password(password):
		# 	raise forms.ValidationError("Incorrect password")
				
		return super(UserLoginForm,self).clean(*args,**kwargs)


class RegistrationForm(forms.ModelForm):
	username = forms.CharField(label = 'User Name',help_text=False)
	email = forms.EmailField(label = 'Email Address')
	email2 = forms.EmailField(label = 'Confirm Email')
	password = forms.CharField(widget = forms.PasswordInput)
	ppassword = forms.CharField(widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]

	def clean(self,*args,**kwargs):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Email must match")
		email_qs = User.objects.filter(email= email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return super(RegistrationForm,self).clean(*args,**kwargs)



