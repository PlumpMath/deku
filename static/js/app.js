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


var loginButton = document.querySelector("#login-button");

var app = app || {};

if ($("#login-button").is(":visible")) {
	new app.CreateView();
} else {
	new app.HandView({vent: vent});
}

/*
 * This will close all menus.
 */
function closeAll() {
	$('.collapsed').removeClass('expanded')
	.children().hide('medium');
};

/*
 * When the slidebar is open, clicking anywhere but the menu closes that menu.
 * To prevent the tab from being stuck on the page, this tracks clicks to the page
 * If the bar is open and the click is NOT on the bar, call closeTab() to properly
 * close the tab and return the tab
 */
$("#sb-site").click(function(event) {
	if (Slidebars.active('right') && !$(event.target).is($("#slidebar-right"))) {
		closeTab();
	}
});

//A Slidebars instance
var Slidebars = new $.slidebars();

//This tracks events for the tabbutton
var tabButton = document.querySelector("#menu-tab");

//by default the slidebar is NOT open
var open = false;

/*
 * This tracks the click events on the tab.
 * If the bar is closed (open is false) run the open function.
 * Otherwise run close
 */
tabButton.onclick = function(event) {
	//$.slidebars();
	//Slidebars.toggle('right');
	var offset = parseInt($('#slidebar-right').css('width'), 10);
	if (!open) {
		Slidebars.open('right');
		openTab(offset);
	} else {
		Slidebars.close('right');
		closeTab();
	}
};

/*
 * This opens the slidebar and moves the tab with it.
 */
function openTab(offset) {
	$("#tab-container").animate({
		marginRight: offset+'px'
	},
 	{duration: 400, easing: 'linear'});
	$("#menu-tab").html("&#9654;");
	open = !open;
};

/*
 * This closes the menu and returns the tab to the proper place
 */
function closeTab() {
	$("#tab-container").animate({
		marginRight: '0px'
	},
	{duration: 200, easing: 'linear'});
	$("#menu-tab").html("&#9664;");
	open = !open;
};

loginButton.onclick = function(event) {
	event.preventDefault();
	$("#container").fadeOut(350);
	setTimeout(function() {new app.LoginView();}, 350);
};
