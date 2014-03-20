var app = app || {};

app.SearchView = Backbone.View.extend({

	el: "#search",

  template: _.template( $('#search-view').html() ),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	}

});
