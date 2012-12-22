var minLeftHeight;
var minRightHeight;

var parentDiv;
var leftDiv;
var rightDiv;


function init() {
	parentDiv = document.getElementById('frontContent');
	leftDiv = document.getElementById('leftColumn');
	rightDiv = document.getElementById('rightColumn');
	minLeftHeight = document.getElementById('leftColumn').offsetHeight;
	minRightHeight = document.getElementById('rightColumn').offsetHeight;
	resizeDivs();
}


function resizeDivs() {
	desiredHeight = getDocHeight()
			- document.getElementById('frontHeader').offsetHeight
			- document.getElementById('footerHandler').offsetHeight
            - 20 	// page's margins
            - 2	 	// page's borders
			- 20;	// columns' margins
	desiredHeight = Math.max(desiredHeight, minLeftHeight);
	desiredHeight = Math.max(desiredHeight, minRightHeight);
	leftDiv.style.height = desiredHeight + 'px';
	rightDiv.style.height = desiredHeight + 'px';
    parentDiv.style.height = desiredHeight + 20 + 'px'; // + 20 = column's margins
}


// In case of problems:
// http://james.padolsey.com/javascript/get-document-height-cross-browser/
function getDocHeight() {
	return window.innerHeight;
}


$(window).resize(resizeDivs);