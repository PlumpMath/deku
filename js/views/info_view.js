var app = app || {};

app.InfoView = Backbone.View.extend({
  el: '#container',

  template: "#info-form",

  events: {
		"submit #info": "getLogin"
	},

  initialize: function() {
    this.render(); 
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    this.$el.html(template).fadeIn(350);

    class_list = ["CMSC 304", "CMSC 345", "CMSC 313", "CMSC 331", "CMSC 341", "STAT 355", "CMSC 201", "CMSC 202"];

    /* Sets the classes field to accept tags, good for autocomplete purposes as well.
     * Currently hardcoded in a bunch of classes. This should be coming from the database and populating an array.
     */
    $('#classes').tagit({
      availableTags: class_list,
      removeConfirmation: true,
      allowSpaces: true,
      beforeTagAdded: function(event, ui) {
        // this makes sure the class you entered is a real class
        if ($.inArray(ui.tagLabel.trim(), class_list) === -1) {
          $('.ui-widget-content').val('')
          .attr('placeholder', 'Enter a valid class');
          return false;
        } else {
          return true;
        }
      }
    });
    $('.ui-autocomplete-input').addClass('tagit-field');
  },

	formErrors: function(values) {
		error = false;
    major_list = $('#major').children().map(function() { return this.value;}).get();
    year_list = $('#year').children().map(function() { return this.value;}).get();

		if (values.bio === '') {
			error = true;
			$('#bio').val('')
			.attr('placeholder', 'Please tell us something about yourself')
      .focus();
		}

    // Make sure the user enters at least one class.		
    if (values.classes.length === 0) {
			error = true;
      $('.ui-widget-content').val('')
      .attr('placeholder', 'Enter a valid class')
      .focus();
		}

		/* Right now this only checks for an empty string.
		 * Eventually it should compare against the possible list of options
		 * and reject it if it does not match something in it.
     */
		if (values.major === '' || $.inArray(values.major, major_list) === -1) {
			error = true;
			$('#major-list').val('')
			.attr('placeholder', 'Please select your major from the given list')
      .focus();
		}

		//eventually, we might want to consider adding an upper bound
		//to the grad year
		if (values.grad_year === '' || $.inArray(values.grad_year, year_list) === -1){
			error = true;
			$('#grad-year').val('')
			.attr('placeholder', 'Please enter a valid graduation year')
      .focus();
		}

		return error;
	},

  getLogin: function(event) {
    event.preventDefault();

    var url = "http://localhost:4568/deku/api/users";

    var that = this;

    // take the classes that are stored in the tags. That's it
    var class_array = $('#classes').tagit('assignedTags');
	
    // new info from this view, attributes match up with what database expects	
		values = {
			grad_year: $('#grad-year').val(),
			major: $('#major-list').val(),
			classes: class_array,
			bio: $('#bio').val().trim()
		};

		if (!this.formErrors(values)) {
      app.user.set(values);
      // app.user holds all the data we need, send a JSON packet of that to the server
      $.post(url, app.user.toJSON(), function(data, textStatus, jqXHR) {
        // navigate to the profile route, clear the user since we don't need it anymore until login
        app.user.set(app.user.defaults());
    	  app.router.navigate('login', {trigger: true});
      }).fail(function(error) {
        bootbox.alert(error);
        console.log(error);
      });
		}
  }
});
