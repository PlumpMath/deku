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
        console.log('reset for search');
        console.log(data['cards']);
        that.reset(data['cards']);
      }
    });
  },
 
  /* sync for cards 
   * When a card is created or updated, it will pull that new data straight from the server.
   */
  sync: function(method, model, options) {
    var that = this;
    if (method === 'create') { // HTTP POST
      $.ajax({
        type: 'POST',
        url: this.url,
        data: model,
        success: function(data) {
          // if it saved to database fine, then add card to view using returned data
          that.add(data['card']);
        },
        fail: function(data) {}
      });
    } else if (method === 'read') { // HTTP GET
    } else if (method === 'update') { // HTTP PUT
    } else if (method === 'delete') { // HTTP DELETE
    }
  }
});
