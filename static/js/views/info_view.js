var InfoView = Backbone.View.extend({
  el: '#container',

  template: _.template( $('#info-form').html() ),

  events: {
		"submit #info": "getLogin"
	},

  initialize: function() {
    this.render(); 
  },

  render: function() {
    this.$el.html(this.template).fadeIn(350);
  },

  getLogin: function(event) {
    event.preventDefault();
		this.$el.fadeOut(350, function() {new LoginView();});
  }
});
