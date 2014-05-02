var app = app || {};

app.User = Backbone.Model.extend({
    defaults: function() {
      return {
        id: -1,
        role: -1,
        firstName: "",
        lastName: "",
        email: "",
        university: "",
        bio: "",
        classes: new Array(),
        grad_year: "",
        major: "",
        avatar: "",
        notifications: [],
        following: [],
        followedBy: []
      }
    }
});
