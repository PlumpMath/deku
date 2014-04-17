var app = app || {};

app.Router = Backbone.Router.extend({
  routes: {
    '': 'homeView',
    'login': 'login'
  },

  homeView: function() {
    new app.AppView();
  },

  login: function() {
    new app.LoginView();
  }
});
