var app = app || {};

app.NotificationView = Backbone.View.extend({

	el: "#notifications",

  template: "#notification-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON())
		this.$el.append(html);
	}

});
