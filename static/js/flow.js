var container = document.querySelector('#container');
var msnry = new Masonry( container, {
    // Masonry options
    columnWidth: 60,
    itemSelector: '.post',
    gutter: 10
});

/**
 * This generates a random color and appends it to an element.
 */

/*
 * This is now unused since cards background is white.
 * Keeping the code in case it is needed later
function setRandomColor(elem) {
    var r = Math.floor(Math.random() * 255),
        g = Math.floor(Math.random() * 255),
        b = Math.floor(Math.random() * 255);

    elem.style.background = "rgb(" + r + ", " + g + ", " + b + ")";
}
*/

/**
 * This function adds random colors to the post blocks.
 */

/*
 * Defaulted to white background for cards, so this is unused
 * keeping this around just in case.
function setRandomColors() {
    var posts = document.querySelectorAll('.post'),
        numPosts = posts.length,
        count = 0;

    for (count; count < numPosts; count++) {
        setRandomColor(posts[count]);
    }
}
*/

//window.onload = setRandomColors();

/**
var addButton = document.querySelector('#addStuff');
addButton.onclick = function(event) {
	//takes the text in the card-textarea
	text = document.getElementById("card-textarea");
	
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
*/
