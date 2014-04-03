var app = app || {};

app.Card = Backbone.Model.extend({
  // define as a function because one field is an array
  defaults: function() {
    return {
      category: "",
	  	tags: new Array(),
      content: "",
      author: "",
      time: "",
      date: "",
      marks: 0,
      adds: 0,
      comments: new Array(),
      popularity: 0
    }
  }

});
