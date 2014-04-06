var app = app || {};

app.FilterView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'filter',

  events: {
    'click': 'deleteFilter'
  },

  template: _.template( $('#filter-view').html() ),
  
	initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template(this.model.toJSON() ) );
		return this;
  },

  deleteFilter: function(event) {
    event.preventDefault();
    var model = this.model;
    this.model.destroy();
    this.remove();
  }
});
