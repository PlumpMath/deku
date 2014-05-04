var app = app || {};

app.CardView = Backbone.View.extend({

  tagName: 'div',
  
  className: 'card post small flipbox',

  template: "#card-template",

  events: {
    "click #car-auth": "goToProfile",
    "click #ins-auth": "goToProfile",
    "click": "flipInspect",
    "click #flip-return": "flipCard",
    "click #post-comment": "postComment",
    "click #comment-btn": "goToComment",
    "click #marks-btn": "markCard",
    "click #adds-btn": "addCard",
    "click #report-joker": "reportJoker",
    "click #hide-card": "hideCard",
    "click #delete-card": "deleteCard",
    "click #user-profile-comment": "goToCommenterProfile",
    "click #delete-comment": "deleteComment"
  },

	initialize: function() {
    // this code shouldn't run, render is called in hand and on updates, it was causing duplicates
    //this.listenTo(this.model, "change", this.render());
    //this.render();
  },

  render: function() {
    this.$el.empty();
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.append(html);
    // can't delete unless it is your card or if you are admin
    if (this.model.get('author_id') !== app.user.get('id')) {
      if (app.user.get('role') !== 2) {
        if ($('#delete-card').is(':visible')) {
          $('#delete-card').remove();
        }
      }
      if ($.inArray(this.model.get('id'), app.user.get('cardsHidden')) !== -1) {
        $('#hide-card').html("Unhide");
      }
    } else {
      $('#hide-card').remove();
    }
    // buttons are different color if user has already added or marked
    if ($.inArray(app.user.get('id'), this.model.get('marks')) !== -1) {
      $('#marks-btn').removeClass('btn-success')
      .addClass('btn-primary');
    }
    if ($.inArray(app.user.get('id'), this.model.get('adds')) !== -1) {
      $('#adds-btn').removeClass('btn-success')
      .addClass('btn-primary');
    }

    if ($.inArray(app.user.get('id'), this.model.get('reporters')) !== -1) {
      $('#report-joker').removeClass('btn-success')
      .addClass('btn-danger');
    }

    /* Really simple scaling check for the cards. For the final demo this should be more realistic,
     * but it is small numbers for testing.
     * Right now it has three tiers
     */
    if (this.model.get('popularity') > 10) {
      this.$el.addClass('large');
    } else if (this.model.get('popularity') > 5) {
      this.$el.addClass('medium');
    } else {
      this.$el.addClass('small');
    }
    if ($.inArray(this.model.get('author_id'), app.user.get('following')) !== -1) {
      this.$el.addClass('following');
    } else {
      this.$el.removeClass('following');
    }
		return this;
  },

  markCard: function(event) {
    event.preventDefault();
    var marks_list = this.model.get('marks'),
        that = this;
    // if the user has NOT marked the card
    $.ajax({
      type: 'POST',
      url: "http://localhost:4568/deku/api/cards/mark/" + this.model.get('id'),
      data: { user_id: app.user.get('id') },
      success: function(data, textStatus, jqXHR) {
        that.model.set(data, {silent: true});
        that.render();
      },
      fail: function() {
      }
    });
  },

  addCard: function(event) {
    event.preventDefault();
    var adds_list = this.model.get('adds'),
        that = this;
    $.ajax({
      type: 'POST',
      url: "http://localhost:4568/deku/api/cards/add/" + this.model.get('id'),
      data: { user_id: app.user.get('id') },
      success: function(data, textStatus, jqXHR) {
        that.model.set(data, {silent: true});
        that.render();
      },
      fail: function() {
      }
    });
  },

  goToComment: function(event) {
    event.preventDefault();
    $('#create-comment').focus();
  },

  //this posts a new comment and updates the view in DOM. Don't think it save to collection
  //THAT IS AN ISSUE!
  postComment: function(event) {
    event.preventDefault();
    var text = $('#create-comment').val().trim();
    var that = this;
    // make sure the comment isn't empty
    if (text !== '') {
      // comment data to pass back
      comment = {
        "author_id": app.user.get('id'),
        "content": text
      };
      $.ajax({
        type: 'POST',
        url: 'http://localhost:4568/deku/api/cards/comment/' + this.model.get('id'),
        data: comment,
        success: function(data, textStatus, jqXHR) {
          that.model.set(data, {silent: true}); // set the model data and render again
          that.render();
        },
        fail: function() {
        }
      });
    } else {
      $('#create-comment').attr('placeholder', "You didn't enter a comment");
    }
  },

  //this controls the flipping of the card to inspect
  flipInspect: function(event) {
    event.preventDefault();
    /* if this is the card view, then go to inspect. otherwise leave it alone
     * also don't react if the link was clicked
     */
    if (this.$el.hasClass('card') && !$(event.target).is('a')) {
      //use jQuery UI switchClass for smooth resize
      this.$el.switchClass('card', 'inspect', 1000);
      //switch the templates
      this.template = "#inspect-template";
      var template = app.TemplateCache.get(this.template);
      var elem = template(this.model.toJSON());
      var that = this;
      this.$el.flippy({
        duration: "1000",
        light: "0",
        depth: "0",
        verso: elem,
        onAnimation: function() {
          // really bad way to do it, but flippy doesn't seem to let DOM manip until done
          if (that.model.get('author_id') !== app.user.get('id')) {
            if (app.user.get('role') !== 2) {
              if ($('#delete-card').is(':visible')) {
                $('#delete-card').remove();
              }
            }
            if ($.inArray(that.model.get('id'), app.user.get('cardsHidden')) !== -1) {
              $('#hide-card').html("Unhide");
            }
          } else {
            // user can't hide their own card
            $('#hide-card').remove();
          }
          if ($.inArray(app.user.get('id'), that.model.get('marks')) !== -1) {
            $('#marks-btn').removeClass('btn-success')
            .addClass('btn-primary');
          }
          if ($.inArray(app.user.get('id'), that.model.get('adds')) !== -1) {
            $('#adds-btn').removeClass('btn-success')
            .addClass('btn-primary');
          }
          if ($.inArray(app.user.get('id'), that.model.get('reporters')) !== -1) {
            $('#report-joker').removeClass('btn-success')
            .addClass('btn-danger');
          }
          app.msnry.layout();
        }
      });
    }
  },

  //return to card view. Must reside within the button
  flipCard: function(event) {
    event.preventDefault();
    this.$el.switchClass('inspect', 'card', 1000);
    this.template = _.template($('#card-template').html());
    var elem = this.template(this.model.toJSON());
    this.$el.flippy({
      duration: "1000",
      light: "0",
      depth: "0",
      verso: elem,
      onAnimation: function() {
        app.msnry.layout();
      }
    });
  },

  /* This will route the user to the profile page of the author of this card.
   * It will use the data in the card model and parse the name and get the id
   * The router will handle the rest.
   */
  goToProfile: function(event) {
    event.preventDefault();
    // navigate to the route for the user's profile
    profile = this.model.get('authorFirst') + "/" + this.model.get('authorLast') + '/' + this.model.get('author_id');
    app.router.navigate('profile/' + profile, {trigger: true});
  },

  goToCommenterProfile: function(event) {
    event.preventDefault();
    app.router.navigate('profile/' + $(event.target).attr('name'), {trigger: true});
  },

  // this lets the author of a card to delete their own card
  deleteCard: function(event) {
    event.preventDefault();
    var that = this;
    // validate with password
    bootbox.prompt("To delete this card, enter your password. Be sure you want to do this as you cannot undo this action.", function(result) {
      if (result !== null) {
        if (app.user.get('id') === that.model.get('author_id')) {
          value = {
            'password': result
          };
          var url = "http://localhost:4568/deku/api/cards/delete/" + that.model.get('id');
          $.post(url, value, function(data, textStatus, jqXHR) {
            // card is deleted, remove it.
            that.undelegateEvents();
            that.stopListening();
            app.msnry.layout();
            Backbone.history.loadUrl(Backbone.history.fragment);
          })
          .fail(function() {
            bootbox.alert("Sorry, your password didn't match.");
          });
        } else if (app.user.get('role') === 2) {
          values = {
            'admin_id': app.user.get('id'),
            'admin_password': result
          };
          // route for admin to delete a card
          var url = "http://localhost:4568/deku/api/admin/cards/delete/" + that.model.get('id');
          $.post(url, values, function(data, textStatus, jqXHR) {
            // card is deleted, remove it.
            that.undelegateEvents();
            that.stopListening();
            app.msnry.layout();
            Backbone.history.loadUrl(Backbone.history.fragment);
          })
          .fail(function() {
            bootbox.alert("Sorry, your password didn't match.");
          });
        }
      }
    });
    $('.bootbox-input-text').attr('type', 'password');
  },

  deleteComment: function(event) {
    event.preventDefault();
    value = {
      "comment_id": $(event.target).attr('name')
    };
    var that = this;
    $.ajax({
      type: 'POST',
      url: "http://localhost:4568/deku/api/cards/comment/delete/" + that.model.get('id'),
      data: value,
      success: function(data, textStatus, jqXHR) {
        that.model.set(data, {silent: true});
        that.render();
      },
      fail: function() {
      }
    });
  },

  reportJoker: function(event) {
    event.preventDefault();
    value = { "reporter_id": app.user.get('id') };
    var that = this;
    bootbox.confirm("Are you sure you want to report this card as a joker?", function(result) {
      if (result === true) {
        $.ajax({
          type: 'POST',
          url: 'http://localhost:4568/deku/api/cards/joker/' + that.model.get('id'),
          data: value,
          success: function(data, textStatus, jqXHR) { 
            that.model.set(data);
            that.render();
          },
          fail: function() { console.log("This failed. Fix it, devs."); }
        });
      }
    });
  },

  // This will hide the card
  hideCard: function(event) {
    event.preventDefault();
    value = {"user_id": app.user.get('id') }; //user id
    var that = this;
    var message = '';
    if (Backbone.history.fragment.substring(0,6) === 'hidden') {
      message = "Are you sure you want to see this card in your hand again?";
    } else {
      message = "Are you sure you want to hide this card from your hand? You can unhide it any time from your preferences panel.";
    }
    // confirm the action
    bootbox.confirm(message, function(result) {
      if (result === true) {
        $.ajax({
          type: 'POST',
          url: 'http://localhost:4568/deku/api/cards/hidden/' + that.model.get('id'),
          data: value,
          success: function(data, textStatus, jqXHR) {
            localStorage.setItem('deku', JSON.stringify(data)); // update user model
            app.user.set(data);
            if (Backbone.history.fragment.substring(0, 6) === 'hidden') {
              app.router.navigate('hand', {trigger: true});
            } else {
              that.remove(); // remove the card
              app.msnry.layout(); // layout masonry to fill gap
            }
          },
          fail: function() {
            console.log("Hiding card failed");
          }
        });
      }
    });
  }
});
