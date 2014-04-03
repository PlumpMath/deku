var tab = $('#tab-container');
var container = document.querySelector('#container');

var app = app || {};

app.HandView = Backbone.View.extend({

  el: "#container",

  initialize: function() { 
    _.bindAll(this, "newCard");
    vent.bind("newCard", this.newCard);
    this.collection = new app.Deck();
    this.render();
    this.listenTo(this.collection, 'add', this.renderCard);
  },

  render: function() {
    this.collection.each(function(item) {
      this.renderCard(item);
      }, this);
    tab.show();
    new app.CreateCardView({vent: vent});
    new app.SearchView();
    new app.MessageView();
    new app.NotificationView();
    new app.AccountView();
    new app.PreferencesView();
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

  newCard: function(card) {
    this.collection.add(card);
  }

});
