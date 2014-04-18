var app = app || {};

app.ProfileView = Backbone.View.extend({

  el: "#container",

  template: "#profile_view",

  initialize: function() {
    this.$el.empty();
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.prepend(html).fadeIn(350);
    // A user can't follow themselves
    if (this.model.get('id') === app.user.get('id')) {
      $('#follow-btn').hide();
    }
  }

});
