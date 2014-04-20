var app = app || {};

app.ProfileView = Backbone.View.extend({

  el: "#container",

  template: "#profile_view",

  events: {
    'click #update-btn': 'update'
  },

  initialize: function() {
    this.$el.empty();
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.prepend(html).fadeIn(350);
    // A user can't follow themselves, but they can update their account
    if (this.model.get('id') === app.user.get('id')) {
      $('#follow-btn').hide();
      $('#update-btn').show();
    } else {
      $('#follow-btn').show();
      $('#update-btn').hide();
    }
  },

  update: function(event) {
    event.preventDefault();
    profile = app.user.get('firstName') + "/" + app.user.get('lastName') + '/' + app.user.get('id');
    app.router.navigate('update/' + profile, {trigger: true});
  }

});
