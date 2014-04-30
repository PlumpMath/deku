var app = app || {};

app.SearchView = Backbone.View.extend({

	el: "#search",

  template: "#search-view",

  events: {
    "click #search-category": "searchCategory",
    "click #search-tag": "searchTag",
    "click #search-author": "searchAuthor",
    "click #search-clear": "searchClear"
  },

	initialize: function() {
    var origin;
		this.render(); // render the view
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.append(template);
	},

  // search by category
  searchCategory: function(event) {
    event.preventDefault();
    // if you aren't searching, then store the current route
    if (Backbone.history.fragment.substring(0,6) !== 'search') {
      this.origin = Backbone.history.fragment;
    }
    search = $('#s-category').val().trim(); //our filter for category
    category_list = $('#categories').children().map(function() { return this.value;}).get(); //possible categories
    if (search !== '' && $.inArray(search, category_list) !== -1) {
      // Change the URL to match search
      app.router.navigate('search/category/' + search, {trigger: true});
      $('#s-category').val('');
    } else
    {
      $('#s-category').val('')
      .attr('placeholder', 'Search by category');
    }
  },

  // search by tag
  searchTag: function(event) {
    event.preventDefault();
    // if you aren't searching, then store the current route
    if (Backbone.history.fragment.substring(0,6) !== 'search') {
      this.origin = Backbone.history.fragment;
    }
    search = $('#s-tag').val().trim(); //our filter for category
    if (search !== '') {
      // Change the URL to match search
      app.router.navigate('search/tag/' + search, {trigger: true});
      $('#s-tag').val('');
    } else
    {
      $('#s-tag').val('')
      .attr('placeholder', 'Search by tag');
    }
  },

  // search by author
  searchAuthor: function(event) {
    event.preventDefault();
    // if you aren't searching, then store the current route
    if (Backbone.history.fragment.substring(0,6) !== 'search') {
      this.origin = Backbone.history.fragment;
    }
    search = $('#s-author').val().trim(); //our filter for category
    if (search !== '') {
      $('#s-author').val('');
      // Change the URL to match search
      search = search.replace(" ", "_");
      app.router.navigate('search/author/' + search, {trigger: true});
    } else
    {
      $('#s-author').val('')
      .attr('placeholder', 'Search by author');
    }
  },
  
  //Clear all of the searches
  searchClear: function(event) {
    event.preventDefault();
    // always return to the route you started on
    app.router.navigate(this.origin, {trigger: true});
    $('#filter-by').html('No active search');
  }
});
