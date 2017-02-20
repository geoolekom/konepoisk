$(document).ready(function() {

	function updateRating () {
		var movieIds = Array();

		$('.movie-rating').each(function() {
			movieIds.push($(this).data('movie-id'));
		})

		$.getJSON('/movies/ratings', {ids: movieIds.join(',')} , function(data) {
			for (var i in data) {
				$('.movie-rating[data-movie-id='+i+']').html('<b>' + data[i] + '</b>');
			}
		});
	}

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
				$(movieRating).html('<h2>' + new_rating + '</h2>');
				image_src = $('.bar-chart').attr("src");
				$('.bar-chart').attr("src", image_src+"?"+Math.floor(Math.random()*1000));
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