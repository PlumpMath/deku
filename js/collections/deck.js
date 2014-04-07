var app = app || {};

app.CardList = Backbone.Collection.extend({
  model: app.Card,
  url: 'http://localhost:4568/deku/api/cards',

  fetch: function() {
    var that = this;
    $.ajax({
      type: 'GET',
      url: this.url,
      success: function(data) {
        that.reset(data['cards']);
      }
    });
  },
});
