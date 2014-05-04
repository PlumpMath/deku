var app = app || {};

app.Card = Backbone.Model.extend({
  // define as a function because one field is an array
  defaults: function() {
    return {
      id: -1,
      category: "",
      tags: new Array(),
      colors: new Array(),
      content: "",
      authorFirst: "first",
      authorLast: "last",
      author_id: -1,
      created_at: "",
      marks: new Array(),
      adds: new Array(),
      comments: new Array(),
      popularity: 0,
      reporters: new Array()
    }
  },
});
