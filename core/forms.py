from core.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form


class AdminUserAddForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "email", "password", "is_active")

	def clean_username(self):
		username = self.cleaned_data["username"]
		email = self.cleaned_data["email"]
		try:
			User._default_manager.get(username=username)
			User._default_manager.get(email=email)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['Username or email is already taken.'])

	@staticmethod
	def clean_password():
		password = make_password("password")
		return password


class AdminUserChangeForm(UserChangeForm):

	class Meta:
		model = User
		fields = ("username", "email", "password", "is_active")


class RegistrationForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email")


class LoginForm(Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())


class LogoutForm(Form):
	pass
