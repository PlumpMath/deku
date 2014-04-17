var app = app || {};

app.PassResetView = Backbone.View.extend({

	el: "#container",

	events: {
		"submit #password-reset": "reset"
	},

	template: "#password-reset-form",

	initialize: function() {
    this.listenTo(app.user, 'change', this.destroyView);
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template).fadeIn(350);
	},

	//This function should handle the event a user resets their password
	reset: function(event) {
		event.preventDefault();
	},

  destroyView: function() {
    this.undelegateEvents();
    this.stopListening();
    return this;
  }
});
