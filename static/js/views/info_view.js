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
    this.$el.html(this.template);
  },

  getLogin: function(event) {
    event.preventDefault();
    new LoginView();
  }
/*
	getLogin: function(event) {
		event.preventDefault();
		new LoginView();
	}
*/
});
