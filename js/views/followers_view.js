var app = app || {};

app.FollowersView = Backbone.View.extend({

	el: "#followers",

  template: "#followers-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
	}

});
