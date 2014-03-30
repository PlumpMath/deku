var app = app || {};

app.CardView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'card post small',

  template: _.template( $('#card-template').html() ),
  
	initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template(this.model.toJSON() ) );
		return this;
  }
});
