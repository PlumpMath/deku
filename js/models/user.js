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
  },

  update: function() {
    var that = this;
    $.ajax({
      type: 'GET',
      url: 'http://localhost:4568/deku/api/users/' + app.user.get('id'),
      success: function(data) {
        //console.log("update the user model :", data['user']);
        localStorage.setItem('deku', JSON.stringify(data['user']));
        app.user.set(data['user']);
      }
    });
  }
});
