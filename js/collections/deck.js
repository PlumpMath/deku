var app = app || {};

app.Deck = Backbone.Collection.extend({
  model: app.Card
});
