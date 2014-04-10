var app = app || {};

app.CreateView = Backbone.View.extend({
  el: '#container',

  events: {
    "submit #create": "getInfo"
  },

  template: _.template( $("#create-form").html() ),

  initialize: function() {
    //listens to the changing of app.user to destroy this view
    this.listenTo(app.user, 'change', this.destroyView);
    this.render();
  },

  render: function() {
    this.$el.html(this.template).fadeIn(350);
  },

	formError: function(values) {
		error = false;

		//simple regex for emails. can have upper, lower, -, _, ., and numbers in name
		//and the only hard requirements is .edu
		email_reg = /^\w+([-_.]\w+)*@\w+.edu$/;
    univ_list = $('#university').children().map(function() { return this.value;}).get();

		if (values.password.length < 8) {
			error = true;
			$('#password').val('');
			$('#password').attr('placeholder', 'Your password must be at least 8 characters long');
      $('#password').focus();
		}
	 
  	if (values.university === '' || $.inArray(values.university, univ_list) === -1) {
	    error = true;
		$('#univ').val('');
		$('#univ').attr('placeholder', 'Please select your university from the list');
        $('#univ').focus();
	}

		//test if the email is valid
		if (!email_reg.test(values.email)) {
			error = true;
			$('#email').val('');
			$('#email').attr('placeholder', 'Enter a valid .edu email address');
      $('#email').focus();
		}

		if (values.lastName === '') {
			error = true;
			$('#lastname').val('');
			$('#lastname').attr('placeholder', 'Please enter your last name');
      $('#lastname').focus();
		}

		if (values.firstName === '') {
			error = true;
			$('#firstname').val('');
			$('#firstname').attr('placeholder', 'Please enter your first name');
      $('#firstname').focus();
		}

		return error;
	},

  getInfo: function(event) {
    event.preventDefault();
		//This will contain some event that sends the data to the server
		//for authentication
		//this is the app.py route info
		var url = "http://localhost:4568/deku/api/users";

		//this is the data that is sent
		var registerValues = {
			email: $("#email").val(),
			password: $("#password").val().trim(),
			university: $("#univ").val(),
			firstName: $("#firstname").val().trim(),
			lastName: $("#lastname").val().trim()
		};

    var that = this;
    	
		if (!this.formError(registerValues)) {
      $.post(url, registerValues, function(data, textStatus, jqXHR) {
        //fade out the view and load the infoView
        that.destroyView();
        that.$el.fadeOut(350, function() {new app.InfoView();});
      }).fail(function(error) {
        console.log(error);
      });
		}
  },

  //logic to handle proper destruction of the current view
  destroyView: function() {
    this.undelegateEvents();
    this.stopListening();
    return this;
  }
});
