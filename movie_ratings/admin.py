from django.contrib import admin
from movie_ratings.models import MovieMark, MovieComment

admin.site.register(MovieMark)
admin.site.register(MovieComment)
