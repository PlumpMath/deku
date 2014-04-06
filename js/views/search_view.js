var app = app || {};

app.SearchView = Backbone.View.extend({

	el: "#search",

  template: _.template( $('#search-view').html() ),

  events: {
    "click #search-category": "searchCategory",
    "click #search-clear": "searchClear",
  },

	initialize: function() {
    this.collection = new app.FilterCollection(); //this collection holds everything we are filtering by
		this.render(); // render the view
    this.init(); // initialize all the local variables
    this.listenTo(this.collection, 'add', this.renderFilter); //listen for added filters
    this.listenTo(this.collection, 'remove', this.remove); // listen for removing a filter
	},

  init: function() {
    filter_category = []; //cards in the category filter
    filter_author = [] // cards in the author filter
    filter_tags = [] // cards in the tags filter
    to_hide = []; // all the items to hide
    msnry_items = []; // array to hold the hidden masonry items
  },

	render: function() {
		this.$el.html(this.template);
	},

  searchCategory: function(event) {
    event.preventDefault();
    search = $('#s-category').val().trim(); //our filter for category
    category_list = $('#categories').children().map(function() { return this.value;}).get(); //possible categories
    if (search !== '' && $.inArray(search, category_list) !== -1) {
      //reveal everything, undo filter for the new search
      app.msnry.reveal(msnry_items);
      cards = app.msnry.getItemElements(); //all cards stored in masonry
      search = $('#s-category').val().trim();
      //find all cards that match this search
      //first clear previous category filter
      to_hide = _.difference(to_hide, filter_category);
      //temporary placeholder, need the old version to delete from
      filter_temp = _.reject(cards, function(card) {
        // card vs. inspect view will have different setup
        if ($(card).hasClass('card')) {
          if ($(card).children('#card-category').html() === this.search) {return this}
        } else {
          if ($(card).children('#inspect-content').children('#card-category').html() === this.search) {return this}
        }
      });
      to_hide = _.union(to_hide, filter_temp);
      msnry_items = _.map(to_hide, function(card) { return app.msnry.getItem(card);});
      $('#s-category').val('');
      app.msnry.hide(msnry_items);
      _.map(to_hide, function(card) {card.style.display = 'none';}); 
      app.msnry.layout();
      var filter = new app.Filter({filter: search, field: "category"});
      this.collection.each(function(f) {
        if (f.toJSON().field === "category") {
          this.collection.remove(f); //remove any previous category (only 1 possible) filters
        }
      }, this);
      //put temp back in and add this filter
      filter_category = filter_temp;
      this.collection.add(filter);
    } else
    {
      $('#s-category').val('')
      .attr('placeholder', 'Search by category');
    }
  },

  //this will render a new filter item and put it at the top of the filter area
  renderFilter: function(filter) {
    var filterView = new app.FilterView({model: filter});
    var elem = filterView.render().el;
    $('#filter').prepend(elem);
  },

  //this removes one filter at a time, user clicks a label at a time.
  remove: function(filter) {
    app.msnry.reveal(msnry_items); // reveal everything
    if (filter.toJSON().field === "category") {
      to_hide = _.difference(to_hide, filter_category); // clear to hide from over category
      filter_category = []; // clear the filter array
      msnry_items = _.map(to_hide, function(card) { return app.msnry.getItem(card);});
      app.msnry.hide(msnry_items); // hide the stuff that needs hiding
      _.map(to_hide, function(card) {card.style.display = 'none';}); 
      app.msnry.layout();
    }
    this.render(); //render everything again
  },

  //Clear all of the searches
  searchClear: function(event) {
    event.preventDefault();
    if (to_hide !== []) {
      _.map(to_hide, function(card) {card.style.display = 'visible';});
      app.msnry.reveal(msnry_items);
      app.msnry.layout();
      // reset all of the data
      $('#s-tags').val('');
      $('#s-author').val('');
      $('#s-category').val('');
      this.collection.reset();
      this.render();
      filter_category = []; 
      filter_author = []; 
      filter_tags = []; 
      to_hide = [];
      msnry_items = [];
    }
  }
});
