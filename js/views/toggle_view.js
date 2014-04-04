var app = app || {};

app.ToggleView = Backbone.View.extend({

  el: "#toggle-bars",

  template: _.template($("#toggle-view").html()),

  initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template);
  }

});
