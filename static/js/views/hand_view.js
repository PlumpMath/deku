var app = app || {};

var tab = $('#tab-container');

app.HandView = Backbone.View.extend({

	el: "#container",

	template: _.template($("#hand-view").html()),

  events: {
    "click #addStuff": "addCard"
  },

	initialize: function() { 
    this.render();
	},

	render: function() {
		this.$el.html(this.template);
		tab.show();
		new app.CreateCardView();
		new app.SearchView();
		new app.MessageView();
		new app.NotificationView();
		new app.AccountView();
		new app.PreferencesView();
	}

});
