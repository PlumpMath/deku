var app = app || {};

app.PreferencesView = Backbone.View.extend({

	el: "#my-preferences",

  events: {
    "click #go-to-card": 'goToCard',
    "click #unhide-card": 'unhideCard',
    "click #go-to-user": 'goToUser',
    "click #unhide-user": 'unhideUser'
  },

  template: "#preferences-view",

	initialize: function() {
    this.listenTo(app.user, 'change', this.render);
		this.render();
	},

	render: function() {
    this.$el.empty();
    var template = app.TemplateCache.get(this.template);
    html = template(app.user.toJSON());
		this.$el.append(html);
	},

  // go to see one card only
  goToCard: function(event) {
    event.preventDefault();
    app.router.navigate('hidden/card/' + $(event.target).attr('name'), {trigger: true});
  },

  // handles showing a card
  unhideCard: function(event) {
    event.preventDefault();
    value = {"user_id": app.user.get('id')};
    var that = this;
     $.ajax({
       type: 'POST',
       url: 'http://localhost:4568/deku/api/cards/hidden/' + $(event.target).attr('name'),
       data: value,
       success: function(data, textStatus, jqXHR) {
         localStorage.setItem('deku', JSON.stringify(data)); // update user
         app.user.set(data);
         that.$el.empty(); // reset preferences to reflect change
         that.render();
       },
       fail: function() {
         console.log("Unhiding card failed");
       }
     });
  },

  goToUser: function(event) {
    event.preventDefault();
    // navigate to the route for the user's profile
    profile = $(event.target).attr('name');
    app.router.navigate('profile/' + profile, {trigger: true});
  }
});
