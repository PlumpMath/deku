var app = app || {};

app.PassResetView = Backbone.View.extend({

	el: "#container",

	events: {
		"submit #password-reset": "reset"
	},

	template: _.template($("#password-reset-form").html()),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template).fadeIn(350);
	},

	//This function should handle the event a user resets their password
	reset: function(event) {
		console.log("RESET");
		event.preventDefault();
	}

});
