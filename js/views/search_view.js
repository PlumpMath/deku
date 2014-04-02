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
    msnry_items = [];
	},

  searchCategory: function(event) {
    event.preventDefault();
    app.msnry.reveal(msnry_items);
    search = $('#s-category').val().trim();
    category_list = $('#categories').children().map(function() { return this.value;}).get();
    if (search !== '' && $.inArray(search, category_list) !== -1) {
      cards = $('#container').children().map(function() { return this});
      search = $('#s-category').val().trim();
      items = items.concat(_.filter(cards, function(card) { if (card.children[2].innerHTML === this.search) {return this}}));
      _.uniq(items);
      to_hide = _.difference(cards, items);
      msnry_items = _.map(to_hide, function(card) { return app.msnry.getItem(card);});
      $('#s-category').val('');
      app.msnry.hide(msnry_items);
      _.map(to_hide, function(card) {card.style.display = 'none';}); 
      app.msnry.layout();
      var filter = new app.Filter({filter: search});
      var filterView = new app.FilterView({model: filter});
      var elem = filterView.render().el;
      $('#filter').append(elem);
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
      app.msnry.reveal(msnry_items);
      app.msnry.layout();
      $('#s-tags').val('');
      $('#s-author').val('');
      $('#s-category').val('');
      $('.filter').remove();
      items = [];
      to_hide = [];
      msnry_items = [];
    }
  }
    
});
