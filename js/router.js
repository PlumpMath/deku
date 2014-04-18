var app = app || {};

app.Router = Backbone.Router.extend({
 
  // current view held in #container
  currentView: null,

  // stores the slidebar and toggle view, children of hand view
  slideView: null,

  toggleView: null,

  // a list of all the existing routes
  routes: {
    '': 'home',
    'register': 'register',
    'profile': 'profile',
    'login': 'login',
    'reset_password': 'reset_password',
    'hand': 'hand',
    'search/category/:query': 'search'
  },

  /* This function facilitates view transitions for #container
   * Each time it is called, it will delete the current view, as long as it exists.
   * It will then create the new view that was passed in
   */
  changeView: function(view) {
    if (this.currentView !== null) {
      this.currentView.undelegateEvents();
      this.currentView.stopListening();
    }
    this.currentView = view;
  },

  /* This will create the children views for the hand view.
   * These consist of the slidebar and the toggle view. Since they
   * need to be destroyed when the user logs out, it is wise to track them
   */
  setChildren: function() {
    if (this.slideView !== null && this.toggleView !== null) {
      this.removeChildren();
    }
    this.slideView = new app.SlidebarView();
    this.toggleView = new app.ToggleView();
  },

	// delete the children of the HandView
  removeChildren: function() {
    this.slideView.undelegateEvents();
    this.slideView.stopListening();
    this.toggleView.undelegateEvents();
    this.toggleView.$el.empty();
    this.toggleView.stopListening();
    this.slideView = null;
    this.toggleView = null;
  },

  // Route on main load. Checks log in state and decides what to do
  home: function() {
    var that = this;
    // no logged in user
    if (localStorage.getItem('deku') === null) {
      // go to register
      this.navigate('register', {trigger: true});
    } else {
      // otherwise go to hand
      this.navigate('hand', {trigger: true});
    }
  },

  /* This is the main route for the website, the create account view.
   * A user defaults to this when they are not logged in, and it must properly
	 * remove any content taht might carry over when a user logs out
   */
  register: function() {
    var that = this;
    // do the slidebar and toggle button exist
    if (this.slideView !== null && this.toggleView !== null) {
      // they do, so remove them and close the slidebar (only real permanent solution)
      this.removeChildren();
      app.$slidebars.close();
    }
    $('#container').fadeOut(350, function() {that.changeView(new app.CreateView());});
  },

  // navigation to get to loginView
  login: function() {
    var that = this;
    $('#container').fadeOut(350, function() {that.changeView(new app.LoginView());});
  },

  // navigation to get to InfoView
  profile: function() {
    var that = this;
    $('#container').fadeOut(350, function() {that.changeView(new app.InfoView());});
  },

  // A little bit tricky, this creates the HandView and the associated children (slidebars and toggle)
  hand: function() {
    // is there a logged in user
    if (localStorage.getItem('deku') !== null) {
      /* Yes, we can load the page.
       * This is partly a protection against a user that logged out from using the back button
       * from being able to get back to the main site.
       */
      this.changeView(new app.HandView());
      this.setChildren();
    }
  },

  // Handles navigation to the password reset view
  reset_password: function() {
    var that = this;
    $('#container').fadeOut(350, function() {that.changeView(new app.PassResetView());});
  },

  search: function(query) {
    // TO BE IMPLEMENTED. FOR NOW IT IS A DUMMY ROUTE. Actually, in the end there may be nothing here
  }
});
