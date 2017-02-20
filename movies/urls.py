from django.conf.urls import url
from movies.views import MovieListView, RatingsView, MovieDetailView, EditMovie, AddMovie, DeleteMovie, RateMovie, get_movie_chart
from movie_ratings.views import CommentDetailView, EditComment, AddComment, DeleteComment
from django.contrib.auth.decorators import permission_required


urlpatterns = [
    url(r'^$', MovieListView.as_view(), name='movies_list'),
    url(r'ratings', RatingsView.as_view(), name='ratings'),
    url(r'comments/edit/(?P<pk>\d+)', EditComment.as_view(), name="comment-edit"),
    url(r'comments/add', AddComment.as_view(), name="comment-add"),
    url(r'comments/delete', DeleteComment.as_view(), name="comment-delete"),
    url(r'comments/(?P<pk>\d+)', CommentDetailView.as_view(), name="comment-detail"),
    url(r'edit/(?P<pk>\d+)', EditMovie.as_view(), name="movie_edit"),
    url(r'delete/(?P<pk>\d+)', permission_required('movie.delete')(DeleteMovie.as_view()), name="movie_delete"),
    url(r'add', permission_required('movie.add')(AddMovie.as_view()), name="movie_add"),
    url(r'rate/(?P<pk>\d+)', RateMovie.as_view(), name="rate"),
    url(r'chart/(?P<pk>\d+)', get_movie_chart, name='chart'),
    url(r'(?P<pk>\d+)', MovieDetailView.as_view(), name='detail'),
]