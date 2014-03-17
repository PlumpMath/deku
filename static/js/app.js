//This function will control toggling the menus.
function collapse() {
	//uses ul tags to find contain what is hidden
	$('#collapsed-list').find('li:has(ul)')
   .click(function (event) {
     if (this == event.target) {
        $(this).toggleClass('expanded');
        $(this).children('ul').toggle('medium');
       }
     return false;
    })
		//everything starts off collapsed
    .addClass('collapsed')
    .children('ul').hide();
};
