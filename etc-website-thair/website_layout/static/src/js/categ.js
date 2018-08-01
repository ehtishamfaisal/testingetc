$( document ).ready(function() {

	if ($(window).width() < 500) {
		$('#color-filter').removeClass("in");
		$('#color-filter').css("height", "0px");
		$('#table_style').removeClass("in");
		$('#table_style').css("height", "0px");
		$('#leg_style').removeClass("in");
		$('#leg_style').css("height", "0px");
		$('#pricefilter').removeClass("in");
		$('#pricefilter').css("height", "0px");
		$('.caret').show()
	}
	else {
		$('.caret').hide()
		$('#color-filter').addClass("in");
		$('#color-filter').css("height", "auto");
		$('#table_style').addClass("in");
		$('#table_style').css("height", "auto");
		$('#leg_style').addClass("in");
		$('#leg_style').css("height", "auto");
		$('#pricefilter').addClass("in");
		$('#pricefilter').css("height", "auto");

	}
	
});
