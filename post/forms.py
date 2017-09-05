from django import forms

class InsertPost(forms.Form):
	text  = forms.CharField(
			widget = forms.Textarea,
		)
	# image = forms.FileField(
	# 		# widget = forms.ClearableFileInput,
	# 	)
	image = forms.FileField(
			# widget=forms.ClearableFileInput(attrs={'multiple': True}),
			widget=forms.FileInput(),
			required = False,
		)