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
		this.$emailInput.focus();
	},

	render: function() {
		this.$el.html(this.template).fadeIn(350);
	},

	sendLogin: function(event) {
		event.preventDefault();
		//This will contain some event that sends the data to the server
		//for authentication
		//this is the app.py route info
		var url = '../../../login';
		console.log("Logging in");

		//this is the data that is sent
		var loginValues = {
			email: this.$emailInput.val(),
			password: this.$passwordInput.val()
		};

		//this is the ajax post request
		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data: loginValues,
			success: function(data) {
				console.log(["Login request details: ", data]);
				//console.log("GO TO INDEX: AJAX");
				window.location.replace('');
			},

			error: function() {
				console.log("Login failed");
				alert("Your email or password did not match");
				this.$emailInput.val('');
				this.$passwordInput.val('');
				this.$emailInput.focus();
			}
		});

	},

	//This will open the reset password view
	resetPassword: function(event) {
		event.preventDefault();
		this.$el.fadeOut(350, function() {new PassResetView();});
	}

});
