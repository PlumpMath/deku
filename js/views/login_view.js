var app = app || {};

app.LoginView = Backbone.View.extend({

	el: "#container",

	events: {
		"click #login-button": "sendLogin",
		"reset #login": "resetPassword"
	},

	template: "#login-form",

	initialize: function() {
		this.render();
    this.$emailInput = this.$('#lemail');
    this.$emailInput.focus();
    this.$passwordInput = this.$('#lpassword');
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template).fadeIn(350);
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
    var that = this;
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
            //alert("Welcome, " + app.user.get("firstName") + "!"); // not really useful
            localStorage.setItem('deku', JSON.stringify(data['user']));
            app.user.set(data['user']);
            app.router.navigate('hand', {trigger: true});
        })
        .fail(function() {
            alert("Your email or password did not match.");
            that.$emailInput.val("");
            that.$passwordInput.val("");
            that.$emailInput.focus();
        });
    }
	},

	//This will open the reset password view
	resetPassword: function(event) {
		event.preventDefault();
    //Set the route to the reset password view
    app.router.navigate('reset_password', {trigger: true});
	}
});
