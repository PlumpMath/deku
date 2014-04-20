var app = app || {};

app.CreateCardView = Backbone.View.extend({

	el: "#card",

	events: {
		"click #add": "addCard"
	},

  template: "#card-create-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template);
    $('#tags').tagsinput({
      typeahead: {
        source: ['pies', 'breezeway', 'fire'],
        freeInput: true
      }
    });
	},

  formError: function(values) {
    error = false;
    //get an array with all of the valid categories
    category_list = $('#categories').children().map(function() { return this.value;}).get();

    //if the user has entered no content, let them know. this is an error
    if (values.content === '') {
      error = true;
      $('#content').val('')
      .attr('placeholder', 'Share with your university')
      .focus();
    }

    //There must be at least 1 tag
    if (values.tags.length === 0) {
      error = true;
      $('.ui-widget-content').val('')
      .attr('placeholder', 'Add tags')
      .focus();
    }

    //There must be a category, and it much be from the category list
    if (values.category === '' || $.inArray(values.category, category_list) === -1) {
      error = true;
      $('#category').val('')
      .attr('placeholder', 'Select a category')
      .focus();
    }

    return error;
  },

	addCard: function(event) {
		event.preventDefault();

    /* This code is redundant security. Create card view should not be visible outside of hand route
     * only allow card creation is the current route is hand.
     */
    if (Backbone.history.fragment === 'hand') {
      //This array will have all the tags the user provided. Comma delimited and lowercased
      var tag_array = $('#tags').val().toLowerCase().split(',');
	    //for each tag, remove whitespace around it
  	  tag_array = _.map(tag_array, function(tag) { return tag.trim();});
			var date = new Date();
    	var card_time = date.toLocaleTimeString();
    	var card_day = date.toDateString();
    	//this is the data in a JSON packet
			var formData = {
				category: $('#category').val().trim(),
				tags: tag_array,
        author: app.user.get('firstName') + " " + app.user.get('lastName'),
        author_id: app.user.get('id'),
				content: $('#content').val().trim(),
				//post_time: card_time,
      	//post_date: card_day
			};

    	//this checks the input for validation
    	if (!this.formError(formData)) {
	  		app.Deck.create(formData);
  			$('#category').val('');
  			$('#tags').val('');
  			$('#content').val('');
    	}
      // check the first piece of the fragment for search
    } else if (Backbone.history.fragment.substring(0,6) === 'search') {
      alert("Clear your search before posting a new card!");
    } else if (Backbone.history.fragment.substring(0,7) === 'profile') {
      alert("Return to the home view to post a new card!");
    }
	}
});
