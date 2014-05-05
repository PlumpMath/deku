var app = app || {};

app.NotificationView = Backbone.View.extend({

	el: "#notifications",

  template: "#notification-view",

  events: {
    "click #user-profile-notification": "goToProfile",
    "click #card-notification": "goToCard",
    "click #delete-notification": "deleteNotification"
  },

	initialize: function() {
    this.listenTo(app.user, 'change', this.render());
		//this.render();
	},

	render: function() {
    //console.log('notifications');
    var template = app.TemplateCache.get(this.template);
    var html = template(app.user.toJSON())
		this.$el.append(html);
    if (app.user.get('notifications').length > 0) {
      styles = {
        'fontWeight': '900',
        'color': '#FAA'
      }
      $('#notifications-menu').css(styles);
    } else {
      styles = {
        'fontWeight': '400',
        'color': '#FFF'
      }
      $('#notifications-menu').css(styles);
    }
	},

  /* This will route the user to the profile page of the author of this card.
   * It will use the data in the card model and parse the name and get the id
   * The router will handle the rest.
   */
  goToProfile: function(event) {
    event.preventDefault();
    // navigate to the route for the user's profile
    app.router.navigate('profile/' + $(event.target).attr('name'), {trigger: true});
  },

  // go to see one card only
  goToCard: function(event) {
    event.preventDefault();
    app.router.navigate('card/' + $(event.target).attr('name'), {trigger: true});
  },

  deleteNotification: function(event) {
    event.preventDefault();
    value = {
      "notification_id": $(event.target).attr('name')
    }
    var that = this;
    $.ajax({
      type: 'POST',
      url: "http://localhost:4568/deku/api/users/notification/delete/" + app.user.get('id'),
      data: value,
      success: function(data, textStatus, jqXHR) {
        localStorage.setItem('deku', JSON.stringify(data));
        app.user.set(data, {silent: true});
        that.$el.empty();
        that.render();
      },
      fail: function() {
      }
    })
  }

});
