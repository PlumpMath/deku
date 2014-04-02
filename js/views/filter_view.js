var app = app || {};

app.FilterView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'filter',

  template: _.template( $('#filter-view').html() ),
  
	initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template(this.model.toJSON() ) );
		return this;
  }
});
