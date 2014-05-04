var app = app || {};

app.ProfileView = Backbone.View.extend({

  el: '#container',

  tagName: 'div',

  template: "#profile_view",

  events: {
    'click #update-btn': 'update',
    'click #change-role': 'changeRole',
    'click #delete-user': 'deleteUser',
    'click #follow-btn': 'followUser',
    'click #hide-user': 'hideUser'
  },

  initialize: function() {
    this.$el.empty();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.prepend(html).show();
    /* A user can't follow themselves, but they can update their account
     * Flat out remove any of these buttons so unathurized access can't happen
     */
    if (this.model.get('id') === app.user.get('id')) {
      $('#follow-btn').remove();
      $('#update-btn').show();
    } else {
      $('#follow-btn').show();
      $('#update-btn').remove();
      if ($.inArray(this.model.get('id'), app.user.get('following')) !== -1) {
        $('#follow-btn').html('Unfollow ' + this.model.get('firstName'));
      }
    }
    $('#delete-user').hide();
    // hide the make mod button by default
    $('#change-role').hide();
    // only mods and admins can see someone's role
    if (app.user.get('role') === 0) {
      $('#user-role').remove();
      $("#change-role").remove();
    } else {
      // go through possible roles of the user being viewed
      switch(this.model.get('role')) {
        case 0:
          // if they are a user, you see 'User' and can make a moderator
          $('#user-role').html('| User');
          // only show make mode on users, if you are an admin
          if (app.user.get('role') === 2) {
            $('#change-role').show();
            $('#delete-user').show();
          } else {
            $('#change-role').remove();
            $('#delete-user').remove();
          }
          break;
        case 1:
          // they are Moderator, can't make moderator.
          $('#user-role').html('| Moderator');
          $('#change-role').show();
          $('#change-role').html('Demote');
          break;
        case 2:
          // Admin is admin, they can't do anything to their role
          $('#user-role').html('| Administrator');
          $('#change-role').remove();
          $('#delete-user').remove();
          break;
      }
    }
  },

  update: function(event) {
    event.preventDefault();
    profile = app.user.get('firstName') + "/" + app.user.get('lastName') + '/' + app.user.get('id');
    app.router.navigate('update/' + profile, {trigger: true});
  },

  // Sends request to make this user a moderator
  changeRole: function(event) {
    event.preventDefault();
    
    var url = 'http://localhost:4568/deku/api/admin/users/make_moderator/' + this.model.get('id');
    var message = "To confirm that you want to make " + this.model.get('firstName') + " " + this.model.get('lastName') + " a moderator, please enter your password.";

    if ($('#change-role').html() === 'Demote') {
      url = 'http://localhost:4568/deku/api/admin/users/make_user/' + this.model.get('id');
      message = "To confirm that you want to demote " + this.model.get('firstName') + " " + this.model.get('lastName') + " from a moderator, please enter your password.";
    }    

    bootbox.prompt(message, function(result) {
      if (result !== null) {
        values = {
          admin_id: app.user.get('id'),
          admin_password: result
        }
        // POST LOGIC HERE TO HANDLE THE POST REQUEST
        $.post(url, values, function( data, textStatus, jqXHR ) {
          Backbone.history.loadUrl(Backbone.history.fragment);
        })
        .fail(function() {
          bootbox.alert("Sorry, your password didn't match.");
        });
      }
    });
    // little bit of a cheeky hack to make the prompt input take a password field instead of straight text.
    $('.bootbox-input-text').attr('type', 'password');
  },

  // admin privilege to delete a user
  deleteUser: function(event) {
    event.preventDefault();
    
    var url = 'http://localhost:4568/deku/api/admin/users/delete/' + this.model.get('id');
    var message = "To confirm that you want to delete " + this.model.get('firstName') + " " + this.model.get('lastName') + "'s account, please enter your password.";

    bootbox.prompt(message, function(result) {
      if (result !== null) {
        values = {
          admin_id: app.user.get('id'),
          admin_password: result
        }
        // POST LOGIC HERE TO HANDLE THE POST REQUEST
        $.post(url, values, function( data, textStatus, jqXHR ) {
          app.router.navigate("hand", {trigger: true});
        })
        .fail(function() {
          bootbox.alert("Sorry, your password didn't match.");
        });
      }
    });
    // little bit of a cheeky hack to make the prompt input take a password field instead of straight text.
    $('.bootbox-input-text').attr('type', 'password');
  },

  followUser: function(event) {
    event.preventDefault();
    var url = "http://localhost:4568/deku/api/users/follow/" + this.model.get('id');
    var that = this;
    $.ajax({
      type: 'POST',
      url: url,
      data: { "active_id": app.user.get('id') },
      success: function(data, textStatus, jqXHR) {
        // update local storage as well as this app.user
        localStorage.setItem('deku', JSON.stringify(data));
        app.user.set(data);
        // change button to have appropriate message
        if ($.inArray(that.model.get('id'), app.user.get('following')) !== -1) {
          $('#follow-btn').html('Unfollow ' + that.model.get('firstName'));
        } else {
          $('#follow-btn').html('Follow ' + that.model.get('firstName'));
        }
      },
      fail: function() {
        console.log("Following failed. Check the routes.");
      }
    });
  },

  hideUser: function(event) {
    event.preventDefault();
    var url = "http://localhost:4568/deku/api/users/hidden/" + this.model.get('id');
    var that = this;
    bootbox.confirm("If you hide this user, you will not be able to see anything that they share with your university. You can unhide them at any time from you preferences panel", function(result) {
      if (result === true) {
        $.ajax({
          type: "POST",
          url: url,
          data: { "active_id": app.user.get('id') },
          success: function(data, textStatus, jqXHR) {
            localStorage.setItem('deku', JSON.stringify(data));
            app.user.set(data);
          },
          fail: function() {
            console.log('Hiding user failed');
          }
        });
      }
    });
  }
});
