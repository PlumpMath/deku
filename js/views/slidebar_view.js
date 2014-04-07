var app = app || {};

app.$slidebars = new $.slidebars({
  siteClose: false,
  disableOver: false,
  hideControlClasses: false
});

//custom event for resizing, using to track state of slidebars
_.extend(window, Backbone.Events);
window.onresize = function() {window.trigger('resize');};

app.SlidebarView = Backbone.View.extend({

  el: "#slidebar-right",

  events: {
    "click": "collapse",
  },

  template: _.template($("#slidebar-view").html()),

  initialize: function() {
    //listen for a window resize
    this.listenTo(window, 'resize', _.debounce(this.slidebarsResize, 500));
    this.render();
  },

  render: function() {
    this.$el.html(this.template);
    //this is our slidebar instance
    //create all the views of the submenus within the slidebar
    new app.CreateCardView();
    new app.SearchView();
    new app.MessageView();
    new app.NotificationView();
    new app.AccountView({model: app.user});
    new app.PreferencesView();
    new app.ToggleView();
    //initially, check out window size
    this.slidebarsResize();
    this.initMenu(); //start up the menu
    this.closeAll(); //by default, only card is open
    $("#default").addClass("expanded")
    .children('ul').toggle('medium');
  },

  //checks window size and changes slidebar state if needed
  slidebarsResize: function() {
    //if the window is at least 1200, open by default, navicon is hidden
    if (window.innerWidth >= 1200) {
      $("#toggle-bars").hide();
      app.$slidebars.open('right');
    } else {
      //if it is less, use the toggle button
      $("#toggle-bars").show();
      app.$slidebars.close();
    }
  },

  //This function starts up the menu by adding collapsed to everything
  initMenu: function() {
  	$('#collapsed-list').find('li:has(ul)')
    .addClass('collapsed')
    .children('ul').hide();
  },
 
  //This function will control toggling the menus.
  collapse: function(event) {
    event.preventDefault();
    //this is the target of the click
    var $target = $(event.target);
    //if the target is a list element
    if ($target.is('li')) {
      //if it is not open already
      if (!$target.hasClass('expanded')) {
        this.closeAll(); //close everything and open the target
        $target.toggleClass('expanded')
		 		.children('ul').toggle('medium');
      } else {
        //target is already open, just close it
        $target.toggleClass('expanded')
        .children().hide('medium');
      }
    }
  },

  //This will close all menus.
  closeAll: function() {
    $('.collapsed').removeClass('expanded')
    .children().hide('medium');
  }

});
