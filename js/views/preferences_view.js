var app = app || {};

app.PreferencesView = Backbone.View.extend({

	el: "#my-preferences",

  events: {
    "click #go-to-card": 'goToCard'
  },

  template: "#preferences-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
    html = template(app.user.toJSON());
		this.$el.append(html);
	},

  goToCard: function(event) {

  }
});
