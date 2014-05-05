var app = app || {};

app.FollowersView = Backbone.View.extend({

	el: "#followers",

  events: {
    "click #user-profile-follower": "goToProfile"
  },

  template: "#followers-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(app.user.toJSON());
		this.$el.append(html);
	},

  /* This will route the user to the profile page of the author of this card.
   * It will use the data in the card model and parse the name and get the id
   * The router will handle the rest.
   */
  goToProfile: function(event) {
    event.preventDefault();
    // navigate to the route for the user's profile
    app.router.navigate('profile/' + $(event.target).attr('name'), {trigger: true});
  }
});
