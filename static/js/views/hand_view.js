var app = app || {};

app.HandView = Backbone.View.extend({

	el: "#container",

	template: _.template($("#hand-view").html()),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
		console.log("Render the create card view");
		new app.CreateCardView();
		new app.SearchView();
		new app.MessageView();
		new app.NotificationView();
		new app.AccountView();
		new app.PreferencesView();
	}

});
