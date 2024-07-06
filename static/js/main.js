// preloader
$(document).ready(function ($) {
	$(window).load(function () {
		setTimeout(function(){
			$('.preloader').fadeOut('slow', function () {
			});
		},500); // set the time here
	});  
});