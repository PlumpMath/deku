var app = app || {};

app.AppView = Backbone.View.extend({
  el: "#main",

  events: {
    'click #login-button': 'login'
  },

  initialize: function() {
    this.$slidebars = new $.slidebars();
  },

  login: function(event) {
    event.preventDefault();
    this.$('#container').fadeOut(350);
    setTimeout(function() { new app.LoginView(); }, 350);
  }
});
