var Card = Backbone.Model.extend({
  defaults: {
    content: ""
  },

  initialize: function(content) {
    this.content = content;
  }
});
