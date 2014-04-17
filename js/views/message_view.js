var app = app || {};

app.MessageView = Backbone.View.extend({

	el: "#messages",

  template: "#message-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
	}

});
