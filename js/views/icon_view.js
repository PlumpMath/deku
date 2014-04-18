var app = app || {};

app.IconView = Backbone.View.extend({

  el: "#deku-icon",

  events: {
    'click a': 'refresh'
  },

  template: "#icon-view",

  initialize: function() {
    this.render();
  },

  render: function() {
    template = app.TemplateCache.get(this.template);
    this.$el.html(template);
  },

  /* When the user clicks the 'deku' icon on the navbar, this should act as a content reset.
   * If the user is not logged in, this will take them back to the register view.
   * If they are logged in, it will return to hand view.
   */
  refresh: function(event) {
    // this checks if there is a user logged in
    if (app.user.get('firstName') === '') {
      // the navigate function does NOT reload the current URL. So I need a work around
      if (Backbone.history.fragment === 'register') {
        // so if the current route matches 'register', then reload that same view with history
        Backbone.history.loadUrl(Backbone.history.fragment);
      } else {
        // otherwise, just navigate to the register route
        app.router.navigate('register', {trigger: true});
      }
    } else {
      /* else the user is logged in.
       * Now check if the current URL matches 'hand'
       */
      if (Backbone.history.fragment === 'hand') {
        Backbone.history.loadUrl(Backbone.history.fragment);
      } else {
        app.router.navigate('hand', {trigger: true});
      }
    }
  }
});
