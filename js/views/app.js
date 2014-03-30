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
		if ($('#logout').is(":visible")) {
			new app.HandView();
		} else {
			new app.CreateView();
		}
    this.$slidebars = new $.slidebars();
  },

  login: function(event) {
    event.preventDefault();
    $('#container').fadeOut(350, function() {new app.LoginView();});
  }
});
