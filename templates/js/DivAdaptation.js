var minLeftHeight;
var minRightHeight;


function init() {
	minLeftHeight = document.getElementById('leftBar').offsetHeight;
	minRightHeight = document.getElementById('content').offsetHeight;
	resizeDivs();
}


function resizeDivs() {
	leftDiv = document.getElementById('leftBar');
	rightDiv = document.getElementById('content');
	desiredHeight = 0;
	desiredHeight = getDocHeight()
			- document.getElementById('frontHeader').offsetHeight
			- document.getElementById('frontFooter').offsetHeight;
	desiredHeight = Math.max(desiredHeight, minLeftHeight);
	desiredHeight = Math.max(desiredHeight, minRightHeight);
	leftDiv.style.height = desiredHeight + 'px';
	rightDiv.style.height = desiredHeight + 'px';
}


// TODO: Test in IE
// In case of problems:
// http://james.padolsey.com/javascript/get-document-height-cross-browser/
function getDocHeight() {
	return window.innerHeight;
}


$(window).resize(resizeDivs);