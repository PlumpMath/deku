var app = app || {};

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
    app.Deck = app.Deck || new app.CardList();
    this.listenTo(app.Deck, 'add', this.renderCard);
    this.listenTo(app.Deck, 'reset', this.render);
    if (use.use === 'hand') {
      app.Deck.fetch();
    }
  },

  render: function() {
    app.Deck.each(function(item) {
      this.renderCard(item);
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
