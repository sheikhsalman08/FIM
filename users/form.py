from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegistrationForm(forms.ModelForm):
	email = forms.EmailField(label = 'Email Address')
	email2 = forms.EmailField(label = 'Confirm Email')
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password'
		]

	def clean(self,*args,**kwargs):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Email must mathc")
		email_qs = User.objects.filter(email= email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return super(RegistrationForm,self).clean(*args,**kwargs)



