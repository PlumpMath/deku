var tab = $("#tab-container");

var app = app || {};

app.CreateView = Backbone.View.extend({
  el: '#container',

  events: {
    "submit #create": "getInfo"
  },

  template: _.template( $("#create-form").html() ),

  initialize: function() {
    this.render();
  },

  render: function() {
    this.$el.html(this.template);
		tab.hide();
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

		if (values.lastname === '') {
			error = true;
			$('#lastname').val('');
			$('#lastname').attr('placeholder', 'Please enter your last name');
      $('#lastname').focus();
		}

		if (values.firstname === '') {
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
		var url = '../../../register';

		//this is the data that is sent
		var registerValues = {
			email: $("#email").val(),
			password: $("#password").val().trim(),
			university: $("#univ").val(),
			firstname: $("#firstname").val().trim(),
			lastname: $("#lastname").val().trim()
		};
		
		if (!this.formError(registerValues))
		{
			//this is the ajax post request
			$.ajax({
				url: url,
				type: 'POST',
				dataType: 'json',
				data: registerValues,
				success: function(data) {
					if(typeof data.errors == "undefined"){
						alert("i cant figure out how to do el fadeout thing. get it get it? el=the?");
						$("#container").fadeOut(350, function() {new app.InfoView();});
					}else{
						alert(data.errors);
					}
				},
				error: function() {
					alert('fail');
					$('#email').val('');
					$('#password').val('');
					$('#univ').val('');
					$('#firstname').val('');
					$('#lastname').val('');
				}
			});
			// this is a temporary backdoor. Will be removed once server works
			$('#container').fadeOut(350, function() {new app.InfoView();});
		}
  }

});
