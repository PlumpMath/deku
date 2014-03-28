var tag = $("#tab-container");

var app = app || {};

app.CreateView = Backbone.View.extend({
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
		tag.hide();
  },

  getInfo: function(event) {
    event.preventDefault();
		this.$el.fadeOut(350, function() {new app.InfoView();});
  }

});
