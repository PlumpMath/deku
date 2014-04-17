var app = app || {};

app.Router = Backbone.Router.extend({
  
  currentView: null,

  routes: {
    '': 'homeView',
    'login': 'login'
  },

  changeView: function(view) {
    if (this.currentView !== null) {
      this.currentView.undelegateEvents();
      this.currentView.stopListening();
    }
    this.currentView = view;
  },

  homeView: function() {
    this.changeView(new app.AppView());
  },

  login: function() {
    this.changeView(new app.LoginView());
  }
});
