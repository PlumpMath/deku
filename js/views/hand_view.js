var app = app || {};

app.HandView = Backbone.View.extend({

  el: "#container",

  initialize: function() { 
    new app.SlidebarView();
    app.Deck = new app.CardList();
    app.Deck.fetch({reset:true});
    this.render();
    this.listenTo(app.Deck, 'add', this.renderCard);
    this.listenTo(app.Deck, 'reset', this.render);
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
    //this is the cards content
    var elem = cardView.render().el;
    this.$el.prepend(elem); //add to the container
    app.msnry.prepended(elem); //add to masonry
    app.msnry.layout();
  },
});
