from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView
from movies.models import Movie
from movie_ratings.models import MovieMark, MovieComment
from django.http import JsonResponse, HttpResponse, Http404
from django.template.defaulttags import register
from django.shortcuts import redirect, get_object_or_404
from movies.forms import MovieForm, RateForm, CommentForm
from django.core.urlresolvers import reverse
from django.db.models import Q


@register.filter
def get_value_from_dict(dictionary, key):
	return dictionary.get(key)


@register.filter
def div3(value):
	return value % 3


class MovieListView(ListView):
	template_name = 'movies/movies_list.html'
	model = Movie

	def get_queryset(self):
		return Movie.objects.filter(deleted=False)


class RatingsView(View):

	def get(self, request):
		ids = request.GET.get('ids', '')
		ids = ids.split(',')
		if ids[0] == '':
			movies = dict()
		else:
			movies = {movie.id: movie.get_rating() for movie in Movie.objects.filter(id__in=ids)}
		return JsonResponse(movies)


class MovieDetailView(DetailView):

	template_name = 'movies/movie.html'
	object = None
	model = Movie

	def dispatch(self, request, pk=None, *args, **kwargs):
		try:
			self.object = Movie.objects.filter(pk=pk)\
				.prefetch_related('moviecomment_set__author')\
				.prefetch_related('moviemark_set').get()
		except Movie.DoesNotExist:
			raise Http404('Такого фильма не существует!')
		return super(MovieDetailView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MovieDetailView, self).get_context_data(**kwargs)
		context['movie'] = self.object
		context['comments'] = self.object.moviecomment_set.all()
		context['add_form'] = CommentForm({'author': self.request.user})

		try:
			mark = self.object.moviemark_set.get(author_id=self.request.user.id)
			form = RateForm(instance=mark)
		except MovieMark.DoesNotExist:
			form = RateForm()
		context['rate_form'] = form
		return context


class AddMovie(CreateView):

	template_name = 'movies/movie_form.html'
	model = Movie
	fields = ('title', 'genre', 'poster', 'description', )


class DeleteMovie(RedirectView):

	def dispatch(self, request, pk=None, *args, **kwargs):
		if pk and request.user.is_staff:
			movie = get_object_or_404(Movie, pk=pk)
			movie.deleted = True
			movie.save()
			return super(DeleteMovie, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't delete it.")

	def get_redirect_url(self, *args, **kwargs):
		return reverse('movies:movies_list')


class EditMovie(UpdateView):
	template_name = 'movies/movie_form.html'
	model = Movie
	form_class = MovieForm
	object = None

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.object = get_object_or_404(Movie, pk=pk)
		return super(EditMovie, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(EditMovie, self).get_context_data(**kwargs)
		context['form'] = MovieForm(instance=self.object)
		context['editing_title'] = self.object.title
		return context

	def form_valid(self, form):
		form.save()
		return redirect(reverse('movies:detail', kwargs={'pk': self.object.id}))


class RateMovie(UpdateView):

	def post(self, request, pk=None, *args, **kwargs):
		if 'mark' in request.POST:
			try:
				mark = int(request.POST['mark'])
				if 0 < mark <= 10:
					MovieMark.objects.update_or_create(
						author_id=request.user.id,
						movie_id=pk,
						defaults={'value': mark}
					)
					return HttpResponse(Movie.objects.get(pk=pk).get_rating())
			except:
				raise Http404


def get_movie_chart(request, pk):
	import numpy as np
	from matplotlib.figure import Figure
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	marks = MovieMark.objects.filter(Q(movie__deleted=False) & Q(movie_id=pk))
	fig = Figure(figsize=(5, 0.8+len(marks)*0.6))
	ax = fig.add_subplot(1, 1, 1)
	data = [mark.value for mark in marks]
	labels = [mark.author.username for mark in marks]
	locs = np.arange(1, len(data) + 1)
	ax.barh(locs, data, height=0.8, tick_label=labels)
	ax.set_xlim([0, 10.5])
	fig.subplots_adjust(left=0.4)
	canvas = FigureCanvas(fig)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response
