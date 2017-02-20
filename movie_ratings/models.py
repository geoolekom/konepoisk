from django.db import models
from movies.models import Movie
from properties.models import Authored
from redactor.fields import RedactorField


class MovieMark(Authored):
	value = models.IntegerField(
		blank=True,
		verbose_name='Оценка',
		choices=[(i, i) for i in range(1, 11)]
	)
	movie = models.ForeignKey(
		Movie,
		verbose_name='Оцененный фильм'
	)

	class Meta:
		verbose_name = 'Оценка'
		verbose_name_plural = 'Оценки'

	def __str__(self):
		return "{0}, {1}: {2}".format(self.author, self.movie, self.value)


class MovieComment(Authored):
	content = RedactorField(
		verbose_name=u'Содержание',
		redactor_options={'lang': 'ru', 'focus': True},
		upload_to='media/comments/',
		allow_file_upload=True,
		allow_image_upload=True,
		blank=True
	)
	movie = models.ForeignKey(Movie, verbose_name='Оцененный фильм')

	class Meta:
		verbose_name = 'Рецензия'
		verbose_name_plural = 'Рецензии'

	def __str__(self):
		return "{0}: {1}".format(self.author, self.content)
