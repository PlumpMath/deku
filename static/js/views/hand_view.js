var app = app || {};

var tab = $('#tab-container');

app.HandView = Backbone.View.extend({

	el: "#container",

	template: _.template($("#hand-view").html()),

  events: {
    "click #addStuff": "addCard"
  },

	initialize: function() { 
    this.listenTo(app.Deck, 'change', this.render);
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
	},

  addCard: function() {
    console.log("Making a card.");
    var content = $('card-textarea').val();
    app.Deck.add(new Card(content));
  }
});
