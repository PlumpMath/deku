//This function will control toggling the menus.
function collapse() {
	//uses ul tags to find contain what is hidden
	$('#collapsed-list').find('li:has(ul)')
   .click(function (event) {
		 //This prevents an open tab from being closed and opened
		 if (!$(this).hasClass('expanded')) {
    	 if (this == event.target) {
				 closeAll();
     	   $(this).toggleClass('expanded')
		 		.children('ul').toggle('medium');
     	 }
		 } else {
			 if ($(event.target).is("li")) {
				 $(this).toggleClass('expanded')
		 		.children().hide('medium');
			 }
		 }
     return false;
    })
    .addClass('collapsed')
    .children('ul').hide();
};

var app = app || {};

$(function() {
  new app.AppView();
});

/*
 * This will close all menus.
 */
function closeAll() {
	$('.collapsed').removeClass('expanded')
	.children().hide('medium');
};
