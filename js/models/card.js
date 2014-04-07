var app = app || {};

app.Card = Backbone.Model.extend({
  // define as a function because one field is an array
  defaults: function() {
    return {
      category: "",
	  	tags: new Array(),
      content: "",
      author: "Author",
      post_time: "",
      post_date: "",
      marks: new Array(),
      adds: new Array(),
      comments: new Array(),
      popularity: 0
    }
  },
});
