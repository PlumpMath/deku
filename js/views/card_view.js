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

  flip: function(event) {
    if (this.$el.hasClass('card')) {
      console.log('currently in card mode');
      this.$el.removeClass('card')
      .addClass('inspect');
      app.msnry.layout();
      this.template = _.template($('#inspect-template').html());
      var elem = this.template(this.model.toJSON());
      this.$el.flippy({
        duration: "1000",
        light: "0",
        depth: "0",
        verso: elem
      });
    } else {
      console.log('currently in inspect mode');
      this.$el.removeClass('inspect')
      .addClass('card');
      app.msnry.layout();
      this.template = _.template($('#card-template').html());
      var elem = this.template(this.model.toJSON());
      this.$el.flippy({
        duration: "1000",
        light: "0",
        depth: "0",
        verso: elem
      });
    }
  },
});
