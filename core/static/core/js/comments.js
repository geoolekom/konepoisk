function saveComment (id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var comment = $('.comment-content[data-comment-id=' + id + ']')
	var content = comment.find('textarea').val();
	$.post(
		'comments/edit/' + id, 
		{id: id, content: content,  csrfmiddlewaretoken: csrf},
		function (data) {
			$('.comment-content[data-comment-id=' + id + ']').html(data);
	});
}

function addComment (movie_id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var comment = $('.add-comment-form')
	var content = comment.find('textarea').val();
	$.post(
		'comments/add', 
		{movie_id: movie_id, content: content,  csrfmiddlewaretoken: csrf},
		function (data) {
			$.get('comments/' + data, function (response) {
				$('.comments').append(response);
				$(".redactor-editor").addClass("redactor-placeholder")
				$(".redactor-editor").html("<p>​</p>");
			});
	});
}

function deleteComment (id) {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var comment = $('.comment[data-comment-id=' + id + ']');
	var dialog = $('.delete-confirm').dialog({
		modal: true,
		position: { my: "center", at: "center", of: comment },
		buttons: {
			"Удалить": function () {
				$.post(
					'comments/delete', 
					{id: id, csrfmiddlewaretoken: csrf}, 
					function (data) {
						comment.remove();
				});
				dialog.dialog("close");
			},
			"Отмена": function () {
				dialog.dialog("close");
			}
		}
	})
}

function loadForm (id) {
	$.get('comments/edit/' + id, function (data) {
		var comment = $('.comment-content[data-comment-id=' + id + ']')
		comment.html(data);
		comment.children('.form-group').children('textarea').redactor();
	})
	//$('.comment-entry[data-comment-id=' + id + ']').load('comments/edit/' + id);
}
