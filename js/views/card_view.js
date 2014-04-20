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
    "click #adds-btn": "addCard"
  },

	initialize: function() {
    this.listenTo(this.model, "change", this.render());
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(this.model.toJSON());
    this.$el.append(html);
		return this;
  },

  markCard: function(event) {
    event.preventDefault();
    var marks_list = this.model.get('marks');
    var index = $.inArray(app.user.get('email'), marks_list)
    // if the user has NOT marked the card
    if (index === -1) {
      marks_list.push(app.user.get('email'));
      this.model.save({"marks": marks_list});
      this.render();
    } else {
      //else remove their mark
      marks_list.splice(index,1);
      this.model.save({"marks": marks_list});
      this.render();
    }
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
    comment_list.push({"author": app.user.get('firstName'), "comment": text});
    this.model.save({"comments": comment_list});
    this.render();
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
      this.template = _.template($('#inspect-template').html());
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
  }
});
