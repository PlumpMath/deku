var app = app || {};

app.CardView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'card post small flipbox',

  template: _.template( $('#card-template').html() ),

  events: {
    "click": "flip"
  },

	initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template(this.model.toJSON() ) );
		return this;
  },

  //this controls the flipping of the card
  flip: function(event) {
    //if we are currently on the card
    if (this.$el.hasClass('card')) {
      this.$el.switchClass('card', 'inspect', 1000);
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
    } else {
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
  },
});
