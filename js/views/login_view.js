var app = app || {};

app.LoginView = Backbone.View.extend({

	el: "#container",

	events: {
		"click #login-button": "sendLogin",
		"reset #login": "resetPassword"
	},

	template: _.template($("#login-form").html()),

	initialize: function() {
		this.render();
        this.$emailInput = this.$('#lemail');
        this.$passwordInput = this.$('#lpassword');
	},

	render: function() {
		this.$el.html(this.template).fadeIn(350);
	},

  formError: function(values) {
    error = false;

    if (values.password === '') {
      error = true;
      $('#lpassword').val('')
      .attr('placeholder', 'Enter your password')
      .focus();
    }
    
    if (values.email === '') {
      error = true;
      $('#lemail').val('')
      .attr('placeholder', 'Enter your e-mail associated with this account')
      .focus();
    }

    return error;
  },

	sendLogin: function(event) {
		event.preventDefault();
		//This will contain some event that sends the data to the server
		//for authentication
		//this is the app.py route info
		var url = 'http://localhost:4568/deku/api/users/login';

		//this is the data that is sent
		var loginValues = {
			email: this.$emailInput.val().trim(),
			password: this.$passwordInput.val().trim()
		};
	
    if (!this.formError(loginValues)) {
        $.post(url, loginValues, function( data, textStatus, jqXHR ) {
            app.user = new app.User(data['user']);
            alert("Welcome, " + app.user.get("firstName") + "!");
        })
        .fail(function() {
            alert("Your email or password did not match.");
            $('#lemail').val("");
            $('#lpassword').val("");
            $('#lemail').focus();
        });
    }

	},

	//This will open the reset password view
	resetPassword: function(event) {
		event.preventDefault();
		this.$el.fadeOut(350, function() {new app.PassResetView();});
	}

});
