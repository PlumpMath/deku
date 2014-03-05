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
function setRandomColor(elem) {
    var r = Math.floor(Math.random() * 255),
        g = Math.floor(Math.random() * 255),
        b = Math.floor(Math.random() * 255);

    elem.style.background = "rgb(" + r + ", " + g + ", " + b + ")";
}

/**
 * This function adds random colors to the post blocks.
 */
function setRandomColors() {
    var posts = document.querySelectorAll('.post'),
        numPosts = posts.length,
        count = 0;

    for (count; count < numPosts; count++) {
        setRandomColor(posts[count]);
    }
}

window.onload = setRandomColors();

var addButton = document.querySelector('#addStuff');
addButton.onclick = function(event) {
    event.preventDefault();
    var elem = document.createElement('div'),
        randomNum = Math.floor(Math.random() * 15),
        randomText = chance.sentence({words: randomNum}),
        randomHeight = Math.floor(Math.random() * 3),
        randomWidth = Math.floor(Math.random() * 3),
        heights = ['h1', 'h2', 'h3'],
        widths = ['w1', 'w2', 'w3'];
    elem.innerHTML = '<p>' + randomText + '</p>';
    // Set height/width depending on sentence length
    elem.className = "post " + heights[randomHeight] + " " + widths[randomWidth];
    setRandomColor(elem);
    container.insertBefore(elem, container[0]);
    msnry.prepended(elem);
    msnry.layout();
    container.focus(elem);
}
