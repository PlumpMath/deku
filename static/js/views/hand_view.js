var HandView = Backbone.View.extend({

	el: "#container",

	template: _.template($("#hand-view").html()),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	}

});
