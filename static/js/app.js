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
		 } else {
			 if ($(event.target).is("li")) {
				 $(this).toggleClass('expanded');
				 $(this).children().hide('medium');
			 }
		 }
     return false;
    })
    .addClass('collapsed')
    .children('ul').hide();
};


var loginButton = document.querySelector("#login-button");

var app = app || {};

if ($("#login-button").is(":visible")) {
	//app = new HandView();
	console.log("load create");
	app = new CreateView();
} else {
	console.log("Load hand");
	app = new HandView();
}

loginButton.onclick = function(event) {
	event.preventDefault();
	$("#container").fadeOut(350);
	setTimeout(function() {new LoginView();}, 350);
};

function closeAll() {
	$('.collapsed').removeClass('expanded');
	$('.collapsed').children().hide('medium');
};
