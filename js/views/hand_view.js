var app = app || {};

app.HandView = Backbone.View.extend({

  el: "#container",

  initialize: function() { 
    new app.SlidebarView();
    app.Deck = new app.CardList();
    this.listenTo(app.user, 'set change', this.destroyView);
    this.listenTo(app.Deck, 'add', this.renderCard);
    this.listenTo(app.Deck, 'reset', this.render);
    app.Deck.fetch();
  },

  render: function() {
    console.log('render hand');
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

  destroyView: function() {
    if (app.user.get('firstName') === '') {
      console.log('go away');
      this.undelegateEvents();
      this.$el.empty();
      this.stopListening();
      return this;
    }
  }
});
