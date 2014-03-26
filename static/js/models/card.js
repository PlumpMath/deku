var app = app || {};

app.Card = Backbone.Model.extend({
  defaults: {
    category: "",
		tags: "",
		content: ""
  },

});
