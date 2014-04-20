var app = app || {};

app.HeaderView = Backbone.View.extend({
  el: ".navbar-form",

  loginTemplate: "#login_header",
  logoutTemplate: "#logout_header",

  /* Events for clicking the login and logout buttons
   * should reside within the header view
   */
  events: {
    'click #login-button': 'login',
    'click #logout': 'logout',
    'click #user-profile-name': 'goToProfile'
  },
  
  initialize: function() {
    this.listenTo(app.user, "change", this.render);
    this.render();
  },

  render: function() {
    var localUser = localStorage.getItem('deku'),
        template,
        html;
    if (localUser !== null) {
      template = app.TemplateCache.get(this.logoutTemplate);
      html = template(app.user.toJSON());
      this.$el.html(html);
    } else {
      template = app.TemplateCache.get(this.loginTemplate);
      this.$el.html(template);
    }
  },

  /* This function will simply switch the view to the login page
   * Unless we are already there. Then it does nothing
   */
  login: function(event) {
    event.preventDefault();
    /* this button should do NOTHING if the login view is active
     * this checks to see if container has a header with text Login
     * if it doesn't, then it switches views.
     */
    if ($('#container').has('h1').length !== 0) {
      if ($('#container').children('h1').html() !== "Login") {
        app.router.navigate('login', {trigger: true});
      }
    }
  },

  logout: function(event) {
    event.preventDefault();
    //logging out removes the user for local storage and will clear app.user to defaults
    localStorage.removeItem('deku');
    app.user.set(app.user.defaults());

    // navigate back to the register route
    app.router.navigate('register', {trigger: true});
  },

  // get the user's profile page
  goToProfile: function(event) {
    event.preventDefault();
    // navigate to the route for the user's profile
    profile = app.user.get('firstName') + "/" + app.user.get('lastName') + '/' + app.user.get('id');
    app.router.navigate('profile/' + profile, {trigger: true});
  }
});
