var app = app || {};

app.MessageView = Backbone.View.extend({

	el: "#messages",

  template: _.template( $('#message-view').html() ),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	}

});
