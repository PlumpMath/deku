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
    new app.IconView();
    //When the app loads we want to pull from this id in localStorage.
    //It will be null if there is nothing there
    var deku = JSON.parse(localStorage.getItem('deku'));
	  if (deku !== null){
      app.user.set(deku);
    }
  }
});
