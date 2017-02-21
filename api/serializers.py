from django.contrib.auth import get_user_model
from movies.models import Movie, Genre
from movie_ratings.models import MovieComment, MovieMark
from rest_framework.serializers import ModelSerializer, HyperlinkedRelatedField, ReadOnlyField


class MovieSerializer(ModelSerializer):
	class Meta:
		model = Movie
		depth = 2
		fields = ('id', 'title', 'genre', 'year', 'budget', 'box_office', 'description', 'poster', 'moviemark_set')


class UserSerializer(ModelSerializer):
	class Meta:
		model = get_user_model()
		depth = 2
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'moviecomment_set', 'moviemark_set')


class CommentSerializer(ModelSerializer):
	author = ReadOnlyField(source='author.username')

	class Meta:
		model = MovieComment
		fields = ('id', 'author', 'movie', 'content', )
