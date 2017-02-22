from django.contrib.auth import get_user_model, login, authenticate
from django.views.generic import CreateView, RedirectView, DetailView, FormView, View
from core.forms import RegistrationForm, LoginForm
from movie_ratings.models import MovieMark
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, reverse, get_object_or_404, render
from django.core.signing import Signer, BadSignature
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.db.models import Q

import shutil
import json

signer = Signer()


class RegisterView(CreateView):
	template_name = 'core/register.html'
	model = settings.AUTH_USER_MODEL
	form_class = RegistrationForm

	def form_valid(self, form):
		user = form.save()
		user.is_active = False
		secret = signer.sign(user.username)
		send_mail(
			'Email confirmation',
			'Click to confirm: http://' + settings.HOST + reverse('core:confirm', kwargs={'secret': secret}),
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
			username = signer.unsign(secret)
			user = get_user_model().objects.get(username=username)
			user.is_active = True
			login(self.request, user)
			user.save()
		except BadSignature:
			raise Http404("Wrong secret key!")
		except get_user_model().DoesNotExist:
			raise Http404("User does not exist.")
		return redirect(reverse('movies:movies_list'))


class LoginView(FormView):
	form_class = LoginForm
	template_name = 'core/user.html'
	success_url = '/'

	def form_valid(self, form):
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		data = get_user_model().objects.filter(Q(email=email) & Q(is_active=True))
		if not data:
			return render(self.request, template_name='core/base.html', context={'errors': 'Неправильный Email.'})
		else:
			user = data.get()
			if user.check_password(password):
				login(self.request, user)
				return super(LoginView, self).form_valid(form)
			else:
				return render(self.request, template_name='core/base.html', context={'errors': 'Неправильный пароль'})

	def form_invalid(self, form):
		return render(self.request, template_name='core/base.html', context={'errors': form.errors})


class UserInfoView(DetailView):
	model = get_user_model()
	template_name = 'core/user_info.html'
	marks = None

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.marks = MovieMark.objects.filter(Q(author_id=pk) & Q(movie__deleted=False))
		return super(UserInfoView, self).dispatch(request, *args, **kwargs)


class UploadView(View):

	def get(self, request):
		return HttpResponse("OK")

	def post(self, request):
		file = request.FILES['file']
		server_name = settings.MEDIA_ROOT + "comments/" + str(request.user) + "_" + file.name
		simple_server_name = settings.MEDIA_URL + "comments/" + str(request.user) + "_" + file.name

		destination = open(server_name, "wb+")
		shutil.copyfileobj(file, destination)
		response = {
			'filelink': simple_server_name,
			'filename': file.name,
		}
		return HttpResponse(json.dumps(response), content_type='application/json')
