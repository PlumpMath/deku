var app = app || {};

app.AppView = Backbone.View.extend({
  el: "#main",

  events: {
    'click #login-button': 'login',
    'click #logout': 'logout'
  },

  initialize: function() {
    var container = $("#container");
    app.msnry = new Masonry( container[0], {
      // Masonry options
      columnWidth: 60,
      itemSelector: ".post",
      gutter: 10
    });
    new app.HeaderView();
    //When the app loads we want to pull from this id in localStorage.
    //It will be null if there is nothing there
    var deku = JSON.parse(localStorage.getItem('deku'));
	  if (deku !== null){
      app.user.set(deku);
    }
    //renders headers based on login status
    this.listenTo(app.user, 'change:firstName', this.render);
    this.render();
  },

  render: function() {
	  if (app.user.get('firstName') !== ''){
	    new app.HandView();
  	} else {
  	  $('#container').fadeOut(350, function() {new app.CreateView();});
  	}
  },

  login: function(event) {
    event.preventDefault();
    /* Force a trigger event that will affect any open views.
     * for control purposes only trigger email because we don't want 
     * app.js render to run unless a real user is being added
     */
    app.user.trigger('change', 'email');

    /* this button should do NOTHING if the login view is active
     * this checks to see if container has a header with text Login
     * if it doesn't, then it switches views.
     */
    if ($('#container').has('h1').length !== 0) {
      if ($('#container').children('h1').html() !== "Login") {
        $('#container').fadeOut(350, function() {new app.LoginView();});
      }
    }
  },

  logout: function(event) {
    event.preventDefault();
    //logging out removes the user for local storage and will clear app.user to defaults
    localStorage.removeItem('deku');
    app.user.set(app.user.defaults());
  }
});
