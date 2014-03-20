var app = app || {};

app.AccountView = Backbone.View.extend({

	el: "#my-account",

  template: _.template( $('#account-view').html() ),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	}

});
