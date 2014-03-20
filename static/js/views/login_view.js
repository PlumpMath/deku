var LoginView = Backbone.View.extend({

	el: "#container",

	events: {
		"click #login-button": "sendLogin",
		"reset #login": "resetPassword"
	},

	template: _.template($("#login-form").html()),

	initialize: function() {
		this.render();
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
			email: $("#lemail").val(),
			password: $("#lpassword").val()
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
			}
		});
	},

	//This will open the reset password view
	resetPassword: function(event) {
		event.preventDefault();
		this.$el.fadeOut(350);
		setTimeout(function() {new PassResetView();}, 350);
	}

});
