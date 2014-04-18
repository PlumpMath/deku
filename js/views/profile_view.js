var app = app || {};

app.ProfileView = Backbone.View.extend({

  el: "#container",

  template: "#profile_view",

  initialize: function() {
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.prepend(html);
  }

});
