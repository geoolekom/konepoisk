$(document).ready(function() {
	//	uploading form for login and logout
	$('.login-form').load('/core/login');

	$('textarea').redactor({
		imageUpload: '/core/upload/',
		fileUpload: '/core/upload/',
		callbacks: {
			imageUpload: function (image, json) {
				$(image).attr('width', "50%");
			},
		}
	});

})