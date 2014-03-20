var CardView = Backbone.View.extend({
  template: _.template( $('#card-template').html() ),

  tagName: 'div',
  
  className: 'card small',

  initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.append(this.template(this.model.toJSON() ) );
  }
});
