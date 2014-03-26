var tag = $("#tab-container");

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
		tag.hide();
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
			password: $("#password").val(),
			university: $("#univ").val(),
			name: $("#name").val()
		};
		
		//this is the ajax post request
		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data: registerValues,
			success: function(data) {
				if(typeof data.errors == "undefined"){
					alert("i cant figure out how to do el fadeout thing. get it get it? el=the?");
					$("el").fadeOut(350, function() {new app.InfoView();});
				}else{
					alert(data.errors);
				}
			},
			error: function() {
				alert('fail');
				$('#lemail').val('');
				$('#lpassword').val('');
				$('#lemail').focus();
			}
		});
  }

});
