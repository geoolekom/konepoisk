from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.forms import Form
from django.core.exceptions import ValidationError
from django.db.models import Q


class AdminUserAddForm(UserCreationForm):

	class Meta:
		model = get_user_model()
		fields = ("username", "email", "password", "is_active")

	def clean_username(self):
		username = self.cleaned_data["username"]
		email = self.cleaned_data["email"]
		try:
			get_user_model()._default_manager.get(username=username)
			get_user_model()._default_manager.get(email=email)
		except get_user_model().DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['Username or email is already taken.'])

	@staticmethod
	def clean_password():
		password = make_password("password")
		return password


class AdminUserChangeForm(UserChangeForm):

	class Meta:
		model = get_user_model()
		fields = ("username", "email", "password", "is_active")


class RegistrationForm(UserCreationForm):
	email = forms.EmailField()

	def clean_email(self):
		data = self.cleaned_data['email']
		if not get_user_model().objects.filter(Q(email=data) & Q(is_active=True)):
			return data
		else:
			raise ValidationError('Пользователь с таким email уже есть.')

	class Meta:
		model = get_user_model()
		fields = ("username", "first_name", "last_name", "email")


class LoginForm(Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())


class LogoutForm(Form):
	pass
