var app = app || {};

app.Deck = Backbone.Collection.extend({
  model: app.Card,
  url: 'http://localhost:4568/deku/api/cards'
});
