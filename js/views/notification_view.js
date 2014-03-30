var app = app || {};

app.NotificationView = Backbone.View.extend({

	el: "#notifications",

  template: _.template( $('#notification-view').html() ),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	}

});
