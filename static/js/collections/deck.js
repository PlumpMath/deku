var app = app || {};

var Deck = Backbone.Collection.extend({
  model: Card
});

app.Deck = new Deck();
