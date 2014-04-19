var app = app || {};

app.UpdateAccountView = Backbone.View.extend({

  el: "#container",

  template: "#update-view",

  initialize: function() {
    this.$el.empty();
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(app.user.toJSON());
    this.$el.prepend(html).fadeIn(350);
  }

});
