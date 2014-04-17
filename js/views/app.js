var app = app || {};

app.AppView = Backbone.View.extend({
  el: "#main",

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
  }
});
