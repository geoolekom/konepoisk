$(document).ready(function() {

	function updateRating () {
		var movieIds = Array();

		$('.movie-rating').each(function() {
			movieIds.push($(this).data('movie-id'));
		});

		$.getJSON('/api/movies.json', function(data) {
			for(i = 0; i < data.length; i++) {
				movie_id = data[i]['id'];
				index = movieIds.indexOf(movie_id);
				if (index != -1) {
					$('.movie-rating[data-movie-id='+movie_id+']').html('<b>' + data[i]['rating'].toFixed(2) + '</b>');
				}
			}
		});
	}

	updateRating();
	window.setInterval(updateRating, 1000);

	$('.sort-form').find('select').change(function () {
	    window.location.href = '/movies?sort=' + $(this).val();
	});


	$('.movie_mark').find('select').change(function () {
		var url = $('.movie-rating').data('rate-url');
		var mark_val = $(this).val();
		var movieRating = $('.movie-rating');

		var csrf = $("input[name='csrfmiddlewaretoken']").val();
		$.post(
			url, 
			{mark: mark_val, csrfmiddlewaretoken: csrf},
			function (new_rating) {
				$(movieRating).html('<b>' + new_rating + '</b>');
				image_src = $('.bar-chart').attr("src");
				loadMovieChart();
		});
	});

});

function deletemovie (id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	$.movie(
		'delete',
		{id: id, csrfmiddlewaretoken: csrf}, 
		function (data) {
			if (window.location.href != "/movies") {
				window.location.href = "/movies";
			} else {
				$('.movie[data-movie-id=' + id + ']').remove();
			}
	});
}

function loadMovieChart () {
	var movie_id = $('.movie').data('movie-id');
	$.get('/api/movies/' + movie_id + '.json', function(data) {
		var set = data['moviemark_set'];
		var users = Array();
		var marks = Array();
		for (i = 0; i < set.length; i++) {
			users.push(set[i]['author']['username']);
			marks.push(set[i]['value'])
		}
		var myChart = Highcharts.chart('movie-chart', {
			chart: {
				type: 'bar'
			},
			title: {
				text: 'Статистика оценок'
			},
			xAxis: {
				categories: users
			},
			yAxis: {
				title: {
					text: null
				},
				max: 10
			},
			series: [{
				name: 'Оценка',
				data: marks
			}],
			legend: [{
				enabled: false
			}]
		});
	});
}