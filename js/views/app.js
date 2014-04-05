var app = app || {};

app.msnry = new Masonry( container, {
    // Masonry options
    columnWidth: 60,
    itemSelector: '.post',
    gutter: 10
});

app.AppView = Backbone.View.extend({
  el: "#main",

  events: {
    'click #login-button': 'login'
  },

  initialize: function() {
    new app.HeaderView({ model: app.user });
    //Checks User because I set that as a default for debugging purposes. Will get rid of it soon
	  if (app.user.get("firstName") !== "" && app.user.get("firstName") !== "User"){
	    new app.HandView();
  	} else {
  	  new app.CreateView();
  	}
  },

  login: function(event) {
    event.preventDefault();
    $('#container').fadeOut(350, function() {new app.LoginView();});
  }
});
