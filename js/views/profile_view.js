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
    profile = (app.user.get('firstName') + "_" + app.user.get('lastName')).split(' ');
    route = '';
    // if someone's name has many spaces, this will replace spaces with '_'
    for (p in profile) {
      route += (profile[p] += '_');
    }
    route = route.substring(0, route.length - 1); //chop off the last '_'
    app.router.navigate('update/' + route + '/' + app.user.get('id'), {trigger: true});
  }

});
