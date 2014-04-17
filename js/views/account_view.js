var app = app || {};

app.AccountView = Backbone.View.extend({

	el: "#my-account",

  template: "#account-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		var html = template(app.user.toJSON());
    this.$el.html(html);
	}

});
