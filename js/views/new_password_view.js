var app = app || {};

app.NewPasswordView = Backbone.View.extend({

	el: "#container",

	events: {
		"click #update-password-button": "updatePassword",
	},

	template: "#update-password-form",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template).fadeIn(350);
	},

  formError: function(value) {
    error = false;

    // password must be valid and match with the confirm
    if (value.password.length < 8 || value.password !== $('#confirm-password').val()) {
      error = true;
      $('#password').val('')
      .attr('placeholder', 'Your password must be at least 8 characters long')
      .focus();
      $('#confirm-password').val('')
      .attr('placeholder', 'Confirm your password');
    }

    return error;
  },

  // collects a new password
	updatePassword: function(event) {
		event.preventDefault();
    var that = this;
		var url = 'http://localhost:4568/deku/api/users/password/' + app.user.get('id');

		//this is the data that is sent
		var values = {
			password: $("#password").val().trim()
		};
    if (!this.formError(values)) {
      $.post(url, values, function( data, textStatus, jqXHR ) {
          // Store that user in localStorage for persistent user state.
          localStorage.setItem('deku', JSON.stringify(data));
          app.user.set(data);
          app.router.navigate('hand', {trigger: true});
      })
      .fail(function() {
          bootbox.alert("Try again, there was an error.");
      });
    }
	}
});
