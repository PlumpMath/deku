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
		this.render(); // render the view
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
	},

  searchCategory: function(event) {
    event.preventDefault();
    search = $('#s-category').val().trim(); //our filter for category
    category_list = $('#categories').children().map(function() { return this.value;}).get(); //possible categories
    if (search !== '' && $.inArray(search, category_list) !== -1) {
      // Change the URL to match search
      app.router.navigate('search/category/' + search, {trigger: true});
      $('#filter-by').html('Searching for ' + search);
      $('#s-category').val('');
    } else
    {
      $('#s-category').val('')
      .attr('placeholder', 'Search by category');
    }
  },

  searchTag: function(event) {
    event.preventDefault();
    search = $('#s-tag').val().trim(); //our filter for category
    if (search !== '') {
      // Change the URL to match search
      app.router.navigate('search/tag/' + search, {trigger: true});
      $('#filter-by').html('Searching for ' + search);
      $('#s-tag').val('');
    } else
    {
      $('#s-tag').val('')
      .attr('placeholder', 'Search by tag');
    }
  },

  searchAuthor: function(event) {
    event.preventDefault();
    search = $('#s-author').val().trim(); //our filter for category
    if (search !== '') {
      $('#filter-by').html('Searching for ' + search);
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
    app.router.navigate('hand', {trigger: true});
    $('#filter-by').html('No active search');
  }
});
