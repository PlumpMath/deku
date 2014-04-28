var app = app || {};

app.CardList = Backbone.Collection.extend({
  model: app.Card,
  url: 'http://localhost:4568/deku/api/cards',
  url_search: 'http://localhost:4568/deku/api/cards/search/',

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

  searchBy: function(route) {
    var that = this;
    $.ajax({
      type: 'GET',
      url: this.url_search + route,
      success: function(data) {
        that.reset(data['cards']);
      }
    });
  }
});
