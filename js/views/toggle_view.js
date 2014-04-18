var app = app || {};

app.ToggleView = Backbone.View.extend({

  el: "#toggle-bars",

  template: "#toggle-view",

  events: {
    "click": "toggle"
  },

  initialize: function() {
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    this.$el.html(template);
  },

  //custom toggle event using the Slidebars instance
  toggle: function(event) {
    event.preventDefault();
    app.$slidebars.toggle('right');
  }
});
