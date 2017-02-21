from django.contrib.auth import get_user_model
from movies.models import Movie, Genre
from movie_ratings.models import MovieComment, MovieMark
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework.serializers import ReadOnlyField, FloatField, HyperlinkedRelatedField, PrimaryKeyRelatedField, StringRelatedField, ChoiceField


class CommentSerializer(ModelSerializer):
	author = ReadOnlyField(source='author.username')

	class Meta:
		model = MovieComment
		depth = 1
		fields = ('id', 'author', 'movie', 'content', )


class MarkSerializer(ModelSerializer):
	author = ReadOnlyField(source='author.username')

	class Meta:
		model = MovieMark
		depth = 1
		fields = ('id', 'author', 'movie', 'value', )


class MovieSerializer(ModelSerializer):
	rating = FloatField(read_only=True)
	moviecomment_set = CommentSerializer(many=True)
	moviemark_set = MarkSerializer(many=True)

	class Meta:
		model = Movie
		fields = ('id', 'title', 'rating', 'genre', 'year', 'budget', 'box_office', 'description', 'poster', 'moviecomment_set', 'moviemark_set')


class UserSerializer(ModelSerializer):
	moviecomment_set = CommentSerializer(many=True)
	moviemark_set = MarkSerializer(many=True)

	class Meta:
		model = get_user_model()
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'moviecomment_set', 'moviemark_set')


