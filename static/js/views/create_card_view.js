var app = app || {};

var container = document.querySelector('#container');
var msnry = new Masonry( container, {
    // Masonry options
    columnWidth: 60,
    itemSelector: '.post',
    gutter: 10
});

app.CreateCardView = Backbone.View.extend({

	el: "#card",

	events: {
		"click #addStuff": "addCard"
	},

  template: _.template( $('#card-create-view').html() ),

	initialize: function() {
		this.render();
	},

	render: function() {
		this.$el.html(this.template);
	},

	addCard: function(event) {
		var text = document.getElementById("card-textarea");
	
		//checks the text variable. Does NOT post card
		//if this field is blank!
		if (text.value !== "") {
			//don't refresh
 			event.preventDefault();
			var elem = document.createElement('div'),
					randomNum = Math.floor(Math.random() * 15),
      		//randomText = chance.sentence({words: randomNum}),
      		randomSize = Math.floor(Math.random() * 3),
      		size = ['small', 'medium', 'large'];
    	elem.innerHTML = '<p>' + text.value + '</p>';
    	// Set height/width depending on sentence length
    	elem.className = "post " + size[randomSize];
    	//setRandomColor(elem);
			//cards default to white background
			elem.style.backgroundColor = "#fff";
			//for a more card like look the borders are rounded
			elem.style.borderRadius = "7px";
			elem.style.border = "0px"
  	  container.insertBefore(elem, container[0]);
			//newest cards on top
			msnry.prepended(elem);
			msnry.layout();
    	container.focus(elem);
			//Clear the text field after card is generated
			text.value = "";
		}
	}

});
