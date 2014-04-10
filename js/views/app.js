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
    'click #login-button': 'login',
    'click #logout': 'logout'
  },

  initialize: function() {
    new app.HeaderView({ model: app.user });
    var deku = JSON.parse(localStorage.getItem('deku'));
	  if (deku !== null){
      app.user.set(deku);
    }
    this.listenTo(app.user, 'set change', this.render);
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
    $('#container').fadeOut(350, function() {new app.LoginView();});
  },

  logout: function(event) {
    event.preventDefault();
    localStorage.removeItem('deku');
    app.user.set(app.user.defaults());
  }
});
