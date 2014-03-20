var HandView = Backbone.View.extend({

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
	},

  addCard: function() {
    console.log("Making a card.");
    var content = $('card-textarea').val();
    app.Deck.add(new Card(content));
  }
});
