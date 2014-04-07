var app = app || {};

app.CardList = Backbone.Collection.extend({
  model: app.Card,
  url: 'http://localhost:4568/deku/api/cards'
});
