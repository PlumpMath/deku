var app = app || {};

app.HandView = Backbone.View.extend({

  el: "#container",

  initialize: function() { 
    //this will remove the login view that existed before, or anything else that was present
    this.$el.empty();
    this.$el.show();
    app.msnry = app.msnry || new Masonry( this.$el[0], {
      // Masonry options
      columnWidth: 60,
      itemSelector: ".post",
      gutter: 10
    });
    app.Deck = app.Deck || new app.CardList();
    this.listenTo(app.Deck, 'add', this.renderCard);
    this.listenTo(app.Deck, 'reset', this.render);
    app.Deck.fetch();
  },

  render: function() {
    console.log('render');
    app.Deck.each(function(item) {
      this.renderCard(item);
      }, this);
  },

  renderCard: function(item) {
    console.log('show card');
    var cardView = new app.CardView({
      model: item
    });
    //this is the cards content
    var elem = cardView.render().el;
    this.$el.prepend(elem); //add to the container
    app.msnry.prepended(elem); //add to masonry
    app.msnry.layout();
  }
});
