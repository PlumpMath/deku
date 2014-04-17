var app = app || {};

app.PreferencesView = Backbone.View.extend({

	el: "#my-preferences",

  template: "#preferences-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
	}

});
