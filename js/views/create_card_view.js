var app = app || {};

app.CreateCardView = Backbone.View.extend({

	el: "#card",

	events: {
		"click #add": "addCard"
	},

  template: _.template( $('#card-create-view').html() ),

	initialize: function() {
		this.vent = vent;
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	},

  formError: function(values) {
    error = false;
    category_list = $('#categories').children().map(function() { return this.value;}).get();

    if (values.content === '') {
      error = true;
      $('#content').val('')
      .attr('placeholder', 'Share with your university')
      .focus();
    }

    if (values.tags === '') {
      error = true;
      $('#tags').val('')
      .attr('placeholder', 'Enter tags')
      .focus();
    }

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
    var tag_array = $('#tags').val().split(',');
    console.log("Array before trimming ", tag_array);
    tag_array = _.map(tag_array, function(tag) { return tag.trim();});
    console.log("The array ", tag_array);
		var formData = {
			category: $('#category').val(),
			tags: tag_array,
			content: $('#content').val().trim()
		};

    if (!this.formError(formData)) {
  		var card = new app.Card(formData);

	  	this.vent.trigger("newCard", card);
  		$('#category').val('');
  		$('#tags').val('');
  		$('#content').val('');
    }
	}
});
