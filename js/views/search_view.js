var app = app || {};

app.SearchView = Backbone.View.extend({

	el: "#search",

  template: _.template( $('#search-view').html() ),

  events: {
    "click #search-category": "searchCategory",
    "click #search-clear": "searchClear"
  },

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
    items = [];
    to_hide = [];
	},

  searchCategory: function(event) {
    event.preventDefault();
    app.msnry.reveal(items);
    search = $('#s-category').val().trim();
    category_list = $('#categories').children().map(function() { return this.value;}).get();
    if (search !== '' && $.inArray(search, category_list) !== -1) {
      cards = $('#container').children().map(function() { return this});
      search = $('#s-category').val().trim();
      to_hide = _.reject(cards, function(card) { if (card.children[2].innerHTML === this.search) {return this}});
      items = _.map(to_hide, function(card) { return app.msnry.getItem(card);});
      $('#s-category').val('');
      $('#filter').html(search);
      app.msnry.hide(items);
      _.map(to_hide, function(card) {card.style.display = 'none';}); 
      app.msnry.layout();
    } else
    {
      $('#s-category').val('')
      .attr('placeholder', 'Search by category');
    }
  },

  searchClear: function(event) {
    event.preventDefault();
    if (items !== []) {
      _.map(to_hide, function(card) {card.style.display = 'visible';});
      app.msnry.reveal(items);
      app.l
      app.msnry.layout();
      $('#s-tags').val('');
      $('#s-author').val('');
      $('#s-category').val('');
      $('#filter').html('No filter applied');
      this.filter = [];
      items = [];
    }
  }
    
});
