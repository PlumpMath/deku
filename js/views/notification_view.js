var app = app || {};

app.NotificationView = Backbone.View.extend({

	el: "#notifications",

  template: "#notification-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
	}

});
