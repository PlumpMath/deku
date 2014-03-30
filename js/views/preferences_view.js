var app = app || {};

app.PreferencesView = Backbone.View.extend({

	el: "#my-preferences",

  template: _.template( $('#preferences-view').html() ),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	}

});
