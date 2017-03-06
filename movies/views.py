from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, RedirectView
from movies.models import Movie
from movie_ratings.models import MovieMark
from django.http import HttpResponse, Http404
from django.template.defaulttags import register
from django.shortcuts import redirect, get_object_or_404
from movies.forms import MovieForm, RateForm, CommentForm, SortForm, sort_choices
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg, F, Count


@register.filter
def get_value_from_dict(dictionary, key):
	return dictionary.get(key)


@register.filter
def div3(value):
	return value % 3


class MovieListView(ListView):
	template_name = 'movies/movies_list.html'
	model = Movie
	sort = '-rating'
	
	def dispatch(self, request, *args, **kwargs):
		if 'sort' in request.GET:
			self.sort = request.GET['sort']
		return super(MovieListView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		queryset = Movie.objects\
			.annotate(rating=Avg('moviemark__value')).annotate(pop=Count('moviemark'))\
			.filter(deleted=False)
		if self.sort and self.sort in sort_choices:
			return queryset.order_by(self.sort)
		else:
			return queryset

	def get_context_data(self, **kwargs):
		context = super(MovieListView, self).get_context_data(**kwargs)
		context['sort_form'] = SortForm({'sort': self.sort})
		return context


class MovieDetailView(DetailView):

	template_name = 'movies/movie.html'
	object = None
	model = Movie
	movie_id = None

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.movie_id = pk
		return super(MovieDetailView, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		get_object_or_404()
		try:
			self.object = Movie.objects.filter(pk=self.movie_id)\
				.prefetch_related('moviecomment_set__author')\
				.prefetch_related('moviemark_set').get()
		except Movie.DoesNotExist:
			raise Http404('Такого фильма не существует!')
		return self.object

	def get_context_data(self, **kwargs):
		context = super(MovieDetailView, self).get_context_data(**kwargs)
		context['movie'] = self.object
		context['comments'] = self.object.moviecomment_set.all()
		context['add_form'] = CommentForm({'author': self.request.user})
		context['editing_title'] = self.object.title

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

	def get_context_data(self, **kwargs):
		context = super(AddMovie, self).get_context_data(**kwargs)
		context['editing_title'] = 'Новый фильм'
		return context


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

	def get_success_url(self):
		return reverse('movies:detail', kwargs={'pk': self.object.id})


class RateMovie(UpdateView):

	def post(self, request, pk=None, *args, **kwargs):
		if 'mark' in request.POST:
			mark = request.POST['mark']
			if mark.isdigit() and 0 < int(mark) <= 10:
				MovieMark.objects.update_or_create(
					author_id=request.user.id,
					movie_id=pk,
					defaults={
						'value': mark
					}
				)
				return HttpResponse(get_object_or_404(Movie, pk=pk).get_rating())
