//This function will control toggling the menus.
function collapse() {
	//uses ul tags to find contain what is hidden
	$('#collapsed-list').find('li:has(ul)')
   .click(function (event) {
		 //This prevents an open tab from being closed and opened
		 if (!$(this).hasClass('expanded')) {
    	 if (this == event.target) {
				 closeAll();
     	   $(this).toggleClass('expanded');
     	   $(this).children('ul').toggle('medium');
     	 }
		 }
     return false;
    })
    .addClass('collapsed')
    .children('ul').hide();
};

function closeAll() {
	$('.collapsed').removeClass('expanded');
	$('.collapsed').children().hide('medium');
};
