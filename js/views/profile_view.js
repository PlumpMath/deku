var app = app || {};

app.ProfileView = Backbone.View.extend({

  el: "#container",

  template: "#profile_view",

  events: {
    'click #update-btn': 'update',
    'click #make-mod': 'makeModerator'
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
    // hide the make mod button by default
    $('#make-mod').hide();
    // only mods and admins can see someone's role
    if (app.user.get('role') === 0) {
      $('#user-role').hide();
    } else {
      // go through possible roles of the user being viewed
      switch(this.model.get('role')) {
        case 0:
          // if they are a user, you see 'User' and can make a moderator
          $('#user-role').html('| User');
          // only show make mode on users, if you are an admin
          if (app.user.get('role') === 2) {
            $('#make-mod').show();
          }
          break;
        case 1:
          // they are Moderator, can't make moderator. Could demote though.
          $('#user-role').html('| Moderator');
          break;
        case 2:
          // Admin is admin, they can't do anything to their role
          $('#user-role').html('| Administrator');
          break;
      }
    }
  },

  update: function(event) {
    event.preventDefault();
    profile = app.user.get('firstName') + "/" + app.user.get('lastName') + '/' + app.user.get('id');
    app.router.navigate('update/' + profile, {trigger: true});
  },

  // Sends request to make this user a moderator
  makeModerator: function(event) {
    event.preventDefault();
    // placeholder. make put request to /deku/api/admin/make_moderator/this.model.get('id'), pass in admin id and password (get from bootbox.prompt)
  }
});
