var app = app || {};

app.CardView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'card post small flipbox',

  template: _.template( $('#card-template').html() ),

  events: {
    "click": "flipInspect",
    "click #flip-return": "flipCard"
  },

	initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template(this.model.toJSON() ) );
		return this;
  },

  //this controls the flipping of the card to inspect
  flipInspect: function(event) {
    event.preventDefault();
    //if this is the card view, then go to inspect. otherwise leave it alone
    if (this.$el.hasClass('card')) {
      //use jQuery UI switchClass for smooth resize
      this.$el.switchClass('card', 'inspect', 1000);
      //switch the templates
      this.template = _.template($('#inspect-template').html());
      var elem = this.template(this.model.toJSON());
      this.$el.flippy({
        duration: "1000",
        light: "0",
        depth: "0",
        verso: elem,
        onAnimation: function() {
          app.msnry.layout();
        }
      });
    }
  },

  //return to card view. Must reside within the button
  flipCard: function(event) {
    event.preventDefault();
    this.$el.switchClass('inspect', 'card', 1000);
    this.template = _.template($('#card-template').html());
    var elem = this.template(this.model.toJSON());
    this.$el.flippy({
      duration: "1000",
      light: "0",
      depth: "0",
      verso: elem,
      onAnimation: function() {
        app.msnry.layout();
      }
    });
  }
});
