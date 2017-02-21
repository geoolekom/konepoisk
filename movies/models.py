from django.db import models
from properties.models import Dated, Deletable, Titled
from django.core.urlresolvers import reverse_lazy


class Genre(Titled):
	class Meta:
		verbose_name = 'Жанр'
		verbose_name_plural = 'Жанры'


class Actor(Titled):
	age = models.IntegerField(verbose_name='Возраст')

	class Meta:
		verbose_name = 'Актер'
		verbose_name_plural = 'Актеры'


class Movie(Dated, Deletable, Titled):

	def poster_path(self, filename):
		return 'posters/{0}_{1}'.format(self.title, self.pk)

	genre = models.ForeignKey(Genre, verbose_name='Жанр', null=True, blank=True)
	poster = models.ImageField(verbose_name='Постер', null=True, blank=True, upload_to=poster_path)
	description = models.TextField(verbose_name='Описание', null=True, blank=True)
	year = models.IntegerField(verbose_name='Год выпуска', null=True, blank=True)
	budget = models.IntegerField(verbose_name='Бюджет', null=True, blank=True)
	box_office = models.IntegerField(verbose_name='Сборы', null=True, blank=True)

	def get_rating(self):
		rating = 0
		marks = self.moviemark_set.all()
		if len(marks) > 0:
			for mark in marks:
				rating += mark.value

			return '%.02f' % (rating/len(marks))
		else:
			return '%.02f' % 0

	def get_absolute_url(self):
		return reverse_lazy('movies:detail', kwargs={'pk': self.id})

	class Meta:
		verbose_name = 'Фильм'
		verbose_name_plural = 'Фильмы'


class ActorMovie(models.Model):
	actor = models.ForeignKey(Actor)
	movie = models.ForeignKey(Movie)
