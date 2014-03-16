var InfoView = Backbone.View.extend({
  el: '#container',

  template: _.template( $('#info-form').html() ),

  events: {},

  initialize: function() {
    this.render(); 
  },

  render: function() {
    this.$el.html(this.template);
  }

});
