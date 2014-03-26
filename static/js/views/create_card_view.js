var app = app || {};

app.CreateCardView = Backbone.View.extend({

	el: "#card",

	events: {
		"click #add": "addCard"
	},

  template: _.template( $('#card-create-view').html() ),

	initialize: function() {
		this.vent = vent;
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	},

	addCard: function(event) {
		event.preventDefault();
		var formData = {
			category: $('#category').val(),
			tags: $('#tags').val(),
			content: $('#content').val()
		};

		var card = new app.Card(formData);

		this.vent.trigger("newCard", card);
		$('#category').val('');
		$('#tags').val('');
		$('#content').val('');
	}
});
