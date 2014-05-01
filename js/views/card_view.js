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
    "click #delete-card": "deleteCard",
    "click #user-profile-comment": "goToCommenterProfile"
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
		return this;
  },

  markCard: function(event) {
    event.preventDefault();
    var marks_list = this.model.get('marks');
    var index = $.inArray(app.user.get('id'), marks_list)
    // if the user has NOT marked the card
    if (index === -1) {
      marks_list.push(app.user.get('id'));
      this.model.save({"marks": marks_list});
    } else {
      //else remove their mark
      marks_list.splice(index,1);
      this.model.save({"marks": marks_list});
    }
    this.$el.empty();
    var template = app.TemplateCache.get('#inspect-template');
    var html = template(this.model.toJSON());
    this.$el.append(html);
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
    var comment_list = this.model.get('comments');
    comment_list.push({"author_id": app.user.get('id'), "author_first": app.user.get('firstName'), "author_last": app.user.get('lastName'), "comment": text});
    this.model.save({"comments": comment_list});
    //$('#inspect-comment-list').append(<div class="card-comment"><%=comments[comment].author%>: <%=comments[comment].comment%>);
    this.$el.empty();
    var template = app.TemplateCache.get('#inspect-template');
    var html = template(this.model.toJSON());
    this.$el.append(html);
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
      var template = app.TemplateCache.get('#inspect-template');
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
  }
});
