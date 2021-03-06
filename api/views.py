from django.contrib.auth import get_user_model
from movies.models import Movie, Genre
from movie_ratings.models import MovieComment, MovieMark
from api.serializers import MovieSerializer, UserSerializer, CommentSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework import permissions
from api.permissions import IsAuthorOrReadOnly
from django.db.models import Avg, Count


class MovieList(ListCreateAPIView):
	serializer_class = MovieSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def get_queryset(self):
		queryset = Movie.objects.filter(deleted=False).annotate(rating=Avg('moviemark__value')).annotate(pop=Count('moviemark'))
		if 'sort' in self.request.GET:
			return queryset.order_by(self.request.GET['sort'])
		else:
			return queryset


class MovieDetail(RetrieveUpdateDestroyAPIView):
	queryset = Movie.objects.filter(deleted=False)
	serializer_class = MovieSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class CommentList(ListCreateAPIView):
	queryset = MovieComment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class CommentDetail(RetrieveUpdateDestroyAPIView):
	queryset = MovieComment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class UserList(ListAPIView):
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer

