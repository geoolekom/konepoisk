from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView, RedirectView, DetailView, FormView
from core.forms import RegistrationForm, LoginForm
from movie_ratings.models import MovieMark
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, reverse, get_object_or_404
from django.core.signing import Signer, BadSignature
from django.http import Http404
from django.db.models import Q

signer = Signer()


class RegisterView(CreateView):
	template_name = 'core/register.html'
	model = settings.AUTH_USER_MODEL
	form_class = RegistrationForm

	def form_valid(self, form):
		user = form.save()
		user.is_active = False
		user.secret = signer.sign(user.pk)
		send_mail(
			'Email confirmation',
			'Click to confirm: http://' + settings.HOST + reverse('core:confirm', kwargs={'secret': user.secret}),
			'geoolekom@yandex.ru',
			[user.email],
			fail_silently=True
		)
		user.save()
		return redirect(reverse('core:user', kwargs={'pk': user.id}))


class ConfirmView(RedirectView):
	url = '/'

	def dispatch(self, request, secret=None, *args, **kwargs):
		try:
			pk = signer.unsign(secret)
			user = get_user_model().objects.get(pk=pk)
			user.is_active = True
			login(self.request, user)
			user.save()
		except BadSignature:
			raise Http404("Wrong secret key!")
		return redirect(reverse('movies:movies_list'))


class LoginView(FormView):
	form_class = LoginForm
	template_name = 'core/user.html'
	success_url = '/'

	def form_valid(self, form):
		try:
			user = get_user_model().objects.get(email=form.cleaned_data['email'])
			if user.check_password(form.cleaned_data['password']) and user.is_active:
				login(self.request, user)
				return super(LoginView, self).form_valid(form)
			else:
				form.add_error('password', 'Неправильный пароль.')
				return self.form_invalid(form)
		except get_user_model().DoesNotExist:
			form.add_error('email', 'Нет пользователя с таким email!')
			return self.form_invalid(form)


class UserInfoView(DetailView):
	model = get_user_model()
	template_name = 'core/user_info.html'
	marks = None

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.marks = MovieMark.objects.filter(Q(author_id=pk) & Q(movie__deleted=False))
		return super(UserInfoView, self).dispatch(request, *args, **kwargs)

