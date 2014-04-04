var app = app || {};

app.SlidebarView = Backbone.View.extend({

  el: "#slidebar-right",

  events: {
    "click": "collapse",
  },

  template: _.template($("#slidebar-view").html()),

  initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template);
    //create all the views of the submenus within the slidebar
    new app.CreateCardView({vent: vent});
    new app.SearchView();
    new app.MessageView();
    new app.NotificationView();
    new app.AccountView({model: app.user});
    new app.PreferencesView();
    this.initMenu(); //start up the menu
    this.closeAll(); //by default, only card is open
    $("#default").addClass("expanded")
    .children('ul').toggle('medium');
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
