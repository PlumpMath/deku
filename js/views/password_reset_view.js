var app = app || {};

app.PassResetView = Backbone.View.extend({

	el: "#container",

	events: {
		"click #reset-password-button": "reset"
	},

	template: "#password-reset-form",

    resetURL: "http://localhost:4568/deku/api/users/password",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		this.$el.html(template).fadeIn(350);
	},

  formError: function(values) {
    error = false;

    if (values.email === '') {
      error = true;
      $('#remail').val('')
      .attr('placeholder', 'Enter your e-mail address')
      .focus();
    }

    return error;
  },

	//This function should handle the event a user resets their password
	reset: function(event) {
	  event.preventDefault();
	
      var value = {
		email: this.$('#remail').val().trim(),
	  };
    
      if (!this.formError(value)) {
        $.ajax({
          type: 'POST',
          url: this.resetURL,
          data: value,
          success: function(data, textStatus, jqXHR) {
            bootbox.alert("Please check your email for details on resetting your password.");
          },
          fail: function() {
            console.log("Something failed...");
          }
        });
	  }
    }
});
