var app = app || {};

// global variable to track the refresh interval
var refreshInterval = {};

app.HandView = Backbone.View.extend({

  el: "#container",

  // this extra packet called use is very helpful to prevent duplicate fetching of data
  initialize: function(use) { 
    //this will remove the login view that existed before, or anything else that was present
    if (use.use !== 'search') {
      this.$el.empty();
    }
    this.$el.show();
    app.msnry = new Masonry( this.$el[0], {
      // Masonry options
      columnWidth: 60,
      itemSelector: ".post",
      gutter: 10
    });
    app.Deck = new app.CardList();
    this.listenTo(app.Deck, 'add', this.renderCard);
    this.listenTo(app.Deck, 'reset', this.render);
    var that = this;
    if (use.use === 'hand' && Backbone.history.fragment === 'hand') {
      app.Deck.fetch();
      // set refresh interval to 10 seconds
      refreshInterval = setInterval( function() {
        app.Deck.updateHand();
      }, 10000);
    } else {
      // clear the refresh interval
      clearInterval(refreshInterval);
    }
  },

  render: function() {
    app.Deck.each(function(item) {
      // if a card is under a users hidden field, don't show it
      hidden = [];
      for (var user = 0; user < app.user.get('usersHidden').length; user++) {
        hidden.push(app.user.get('usersHidden')[user].id);
      }
      if ($.inArray(item.get('id'), app.user.get('cardsHidden')) === -1 && $.inArray(item.get('author_id'), hidden) === -1 || Backbone.history.fragment.substring(0,6) === 'hidden')  {
        this.renderCard(item);
      }
    }, this);
  },

  renderCard: function(item) {
    var cardView = new app.CardView({
      model: item
    });
    /* This is the cards content
     * This is where the card is rendered, not with its own init
     */
    var elem = cardView.render().el;
    this.$el.prepend(elem); //add to the container
    app.msnry.prepended(elem); //add to masonry
    app.msnry.layout();
  }
});
