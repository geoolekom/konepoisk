from django.shortcuts import render
from movies.forms import CommentForm
from movies.models import Movie
from movie_ratings.models import MovieComment
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, View
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, reverse


class EditComment(UpdateView):
	template_name = "movies/comment_form.html"
	model = MovieComment
	form_class = CommentForm
	context_object_name = 'comment'

	def get_object(self, queryset=None):
		comment = super(EditComment, self).get_object()
		if comment.author == self.request.user:
			return comment
		else:
			raise Http404("Вы - не автор комментария!")

	def get(self, request, *args, **kwargs):
		self.form = CommentForm(instance=self.get_object())
		return super(EditComment, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		comment = self.get_object()
		if 'content' in request.POST:
			content = request.POST['content']
			setattr(comment, 'content', content)
			comment.save()
			return HttpResponse(content)
		else:
			raise Http404("Нет содержимого!")


class AddComment(CreateView):
	template_name = "movies/add_comment_form.html"
	model = MovieComment
	form_class = CommentForm

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated and 'content' in request.POST and 'movie_id' in request.POST:
			comment = MovieComment(
				author_id=request.user.id,
				content=request.POST['content'],
				movie=get_object_or_404(Movie, pk=request.POST['movie_id'])
			)
			comment.save()
			return HttpResponse(comment.pk)
		else:
			raise Http404


class DeleteComment(DeleteView):
	model = MovieComment
	template_name = "movies/movie.html"
	movie_id = None
	author_id = None

	def get_object(self, queryset=None):
		if 'id' in self.request.POST:
			comment = get_object_or_404(MovieComment, pk=self.request.POST['id'])
			self.movie_id = comment.movie_id
			self.author_id = comment.author_id
			return comment
		else:
			raise Http404('Нет комментария с таким id.')

	def delete(self, request, *args, **kwargs):
		if request.user.id == self.author_id:
			return super(DeleteComment, self).delete(request, *args, **kwargs)
		elif request.user.is_staff:
			comment = self.get_object()
			comment.deleted = True
			comment.save()
			return HttpResponse("hidden")
		else:
			raise Http404('Нет права удалять этот комментарий.')

	def get_success_url(self):
		return reverse('movies:detail', kwargs={'pk': self.movie_id})


class RestoreComment(View):

	def post(self, request, *args, **kwargs):
		if request.user.is_staff and 'id' in request.POST:
			comment = get_object_or_404(MovieComment, pk=self.request.POST['id'])
			comment.deleted = False
			comment.save()
			return HttpResponse("OK")
		else:
			raise Http404('Невозможно восстановить комментарий.')


class CommentDetailView(DetailView):
	model = MovieComment
	template_name = "movies/comment.html"
	context_object_name = 'comment'
