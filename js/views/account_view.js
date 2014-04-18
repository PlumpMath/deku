var app = app || {};

app.AccountView = Backbone.View.extend({

	el: "#my-account",

  events: {
    'click #update-account': "update"
  },

  template: "#account-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		var html = template(app.user.toJSON());
    this.$el.html(html);
	},

  update: function(event) {
    // ACTION PENDING
  }

});
