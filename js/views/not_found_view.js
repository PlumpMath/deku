var app = app || {};

app.NotFoundView = Backbone.View.extend({

  el: "#container",

  template: "#not-found",

  initialize: function() {
    this.render();
  },

  render: function() {
    // basic 404 page
    var template = app.TemplateCache.get(this.template);
    this.$el.html(template).fadeIn(350);
  }

});
