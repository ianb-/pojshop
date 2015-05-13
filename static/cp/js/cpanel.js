$(document).ready(function() {
	$('body').on('click', '.toggle', function() {
		var pid = $(this).attr('data-id');
		var displayed = '<i class="fa fa-toggle-on fa-lg toggle" data-id="'+pid+'"></i>';
		var hidden = '<i class="fa fa-toggle-off fa-lg toggle" data-id="'+pid+'"></i>';
		$.get('/cp/toggle_for_sale/', {pid: pid}, function(data) {
			console.log(data.msg);
			if (data.msg === 'Displayed') {
				$('p', '#p'+pid).html(displayed).toggleClass('text-success text-danger');
			}
			if (data.msg === 'Removed') {
				$('p', '#p'+pid).html(hidden).toggleClass('text-danger text-success');
			}
		});
	});
});