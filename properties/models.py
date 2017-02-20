from django.db import models
from django.conf import settings


class Authored(models.Model):
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name='Автор',
		related_name='+'
	)

	class Meta:
		abstract = True


class Dated(models.Model):
	pub_time = models.DateTimeField(verbose_name='Время публикации', auto_now_add=True)
	upd_time = models.DateTimeField(verbose_name='Последнее изменение', auto_now=True)

	class Meta:
		abstract = True


class Titled(models.Model):
	title = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)

	def __str__(self):
		return self.title

	class Meta:
		abstract = True


class Deletable(models.Model):
	deleted = models.BooleanField(verbose_name='Удален?', default=False)

	class Meta:
		abstract = True
