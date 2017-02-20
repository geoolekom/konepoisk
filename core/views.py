from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView, RedirectView, DetailView, FormView
from core.forms import RegistrationForm, LoginForm
from movie_ratings.models import MovieMark
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, reverse
from django.core.signing import Signer, BadSignature
from django.http import Http404, HttpResponse
from django.db.models import Q

signer = Signer()


class RegisterView(CreateView):
	template_name = 'core/register.html'
	model = settings.AUTH_USER_MODEL
	form_class = RegistrationForm
	success_url = '/core/confirm'

	def form_valid(self, form):
		user = form.save()
		user.is_active = False
		user.secret = signer.sign(user.pk)
		send_mail(
			'Email confirmation',
			'Click to confirm: http://' + settings.HOST + reverse('core:confirm', kwargs={'secret': user.secret}),
			'geoolekom@yandex.ru',
			[user.email],
			fail_silently=False
		)
		user.save()
		return redirect(self.success_url)


class ConfirmView(RedirectView):
	url = '/'

	def dispatch(self, request, secret=None, *args, **kwargs):
		try:
			print(secret)
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
				form.add_error('password', 'Неправильнй пароль.')
				return self.form_invalid(form)
		except get_user_model().DoesNotExist:
			form.add_error('email', 'Нет пользователя с таким email!')
			return self.form_invalid(form)


def get_user_chart(request):
	import numpy as np
	from matplotlib.figure import Figure
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	marks = MovieMark.objects.filter(Q(movie__deleted=False) & Q(author_id=request.user.id))
	fig = Figure()
	ax = fig.add_subplot(1, 1, 1)
	data = [mark.value for mark in marks]
	labels = [mark.movie.title for mark in marks]
	locs = np.arange(1, len(data) + 1)
	width = 0.8
	ax.bar(locs, data, width=width, tick_label=labels)
	ax.set_ylim([0, 10])
	canvas = FigureCanvas(fig)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response


class MarksView(DetailView):
	model = get_user_model()
	template_name = 'core/user_info.html'
	marks = None

	def dispatch(self, request, pk=None, *args, **kwargs):
		if request.user.is_authenticated:
			self.marks = MovieMark.objects.filter(author_id=request.user.id).filter(movie__deleted=False)
			return super(MarksView, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404('Вы не авторизованы!')

	def get_context_data(self, **kwargs):
		context = super(MarksView, self).get_context_data(**kwargs)
		return context





