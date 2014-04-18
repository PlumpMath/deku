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
		
    if (values.classes === '') {
			error = true;
			$('#classes').val('')
			.attr('placeholder', 'Please enter your classes this semester')
      .focus();
		}

		//Right now this only checks for an empty string.
		//Eventually it should compare against the possible list of options
		//and reject it if it does not match something in it.
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

    console.log('user id is: ', app.user.get('id'));

    var url = "http://localhost:4568/deku/api/users";

    var that = this;

    var class_array = $('#classes').val().toLowerCase().split(',');
	  //for each tag, remove whitespace around it
    class_array = _.map(class_array, function(c) { return c.trim();});

    console.log('Classes are: ', class_array);
	
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
        console.log(error);
      });
		}
  }
});
