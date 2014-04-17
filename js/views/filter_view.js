var app = app || {};

app.FilterView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'filter',

  events: {
    'click': 'deleteFilter'
  },

  template: "#filter-view",
  
	initialize: function() {
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.html(html);
		return this;
  },

  deleteFilter: function(event) {
    event.preventDefault();
    var model = this.model;
    this.model.destroy();
    this.remove();
  }
});
