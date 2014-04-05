var app = app || {};

app.ToggleView = Backbone.View.extend({

  el: "#toggle-bars",

  template: _.template($("#toggle-view").html()),

  events: {
    "click": "toggle"
  },

  initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template);
  },

  //custom toggle event using the Slidebars instance
  toggle: function(event) {
    event.preventDefault();
    app.$slidebars.toggle('right');
  }

});
