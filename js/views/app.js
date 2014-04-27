var app = app || {};

app.AppView = Backbone.View.extend({
  el: "#main",

  initialize: function() {
    new app.HeaderView();
    new app.IconView();
    //When the app loads we want to pull from this id in localStorage.
    //It will be null if there is nothing there
    var deku = JSON.parse(localStorage.getItem('deku'));
	  if (deku !== null){
      app.user.set(deku);
    }
  }
});
