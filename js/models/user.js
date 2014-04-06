var app = app || {};

app.User = Backbone.Model.extend({
    defaults: function() {
      return {
        firstName: "",
        lastName: "",
        email: "",
        university: "",
        bio: "",
        classes: new Array(),
        grad_year: "",
        major: ""
      }
    }
});
