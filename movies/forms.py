from django import forms
from movies.models import Movie
from movie_ratings.models import MovieComment, MovieMark

sort_choices = dict([
	("-pub_time", "Новые сверху"),
	("-rating", "Лучшие сверху"),
	("title", "По алфавиту"),
	("-pop", "По популярности"),
])


class SortForm(forms.Form):
	sort = forms.ChoiceField(
		choices=sort_choices.items(),
		label=''
	)


class CommentForm(forms.ModelForm):
	class Meta:
		model = MovieComment
		fields = ('content', )


class MovieForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('title', 'genre', 'year', 'budget', 'box_office', 'poster', 'description', )


class RateForm(forms.ModelForm):
	class Meta:
		model = MovieMark
		fields = ('value', )

