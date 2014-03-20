var CreateView = Backbone.View.extend({
  el: '#container',

  events: {
    "submit #create": "getInfo"
  },

  template: _.template( $("#create-form").html() ),

  initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template);
  },

  getInfo: function(event) {
    event.preventDefault();
		this.$el.fadeOut(350);
    setTimeout(function() {new InfoView();}, 350);
  }

});
