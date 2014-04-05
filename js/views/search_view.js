var app = app || {};

app.SearchView = Backbone.View.extend({

	el: "#search",

  template: _.template( $('#search-view').html() ),

  events: {
    "click #search-category": "searchCategory",
    "click #search-clear": "searchClear",
    "click .filter": "removeFilter"
  },

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
    filter_category = []; //cards in the category filter
    filter_author = [] // cards in the author filter
    filter_tags = [] // cards in the tags filter
    to_hide = []; // all the items to hide
    msnry_items = []; // array to hold the hidden masonry items
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
      filter_category = _.reject(cards, function(card) {
        // card vs. inspect view will have different setup
        if ($(card).hasClass('card')) {
          if ($(card).children('#card-category').html() === this.search) {return this}
        } else {
          if ($(card).children('#inspect-content').children('#card-category').html() === this.search) {return this}
        }
      });
      to_hide = _.union(to_hide, filter_category);
      msnry_items = _.map(to_hide, function(card) { return app.msnry.getItem(card);});
      $('#s-category').val('');
      app.msnry.hide(msnry_items);
      _.map(to_hide, function(card) {card.style.display = 'none';}); 
      app.msnry.layout();
      var filter = new app.Filter({filter: search, field: "category"});
      var filterView = new app.FilterView({model: filter});
      var elem = filterView.render().el;
      $(".category").remove();
      $('#filter').prepend(elem);
    } else
    {
      $('#s-category').val('')
      .attr('placeholder', 'Search by category');
    }
  },

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
      $('.filter').remove();
      filter_category = []; 
      filter_author = []; 
      filter_tags = []; 
      to_hide = [];
      msnry_items = [];
    }
  },

  removeFilter: function(event) {
    event.preventDefault();
    console.log("remove filter");
    var pillBox = $(event.target).html();
    console.log("remove: ", pillBox);
  }
    
});
