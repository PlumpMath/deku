var app = app || {};

app.FollowingView = Backbone.View.extend({

	el: "#following",

  template: "#following-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
	}

});
