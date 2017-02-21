from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import MovieDetail, MovieList, UserList, UserDetail, CommentDetail, CommentList

urlpatterns = [
	url(r'movies/(?P<pk>\d+)', MovieDetail.as_view(), name='movie-detail'),
	url(r'movies/$', MovieList.as_view(), name='movie-list'),
	url(r'users/(?P<pk>\d+)', UserDetail.as_view(), name='user-detail'),
	url(r'users/$', UserList.as_view(), name='user-list'),
	url(r'comments/(?P<pk>\d+)', CommentDetail.as_view(), name='comment-detail'),
	url(r'comments/$', CommentList.as_view(), name='comment-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
