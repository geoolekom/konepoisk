function editLessonForm (id) {

	var dialog = $('.dialog[data-lesson-id=' + id + ']');
	$.get('lessons/edit/' + id, function (data) {
		dialog.html(data);
		var weekday = dialog.data('weekday');
		var group = dialog.data('group');
		console.log(dialog.children("input[name='weekday']"));
		$("input[name='weekday']").attr("value", weekday);
		$("input[name='group']").attr("value", group);
		dialog.dialog();
	});
	
}