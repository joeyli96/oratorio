/**
 * the same jQuery shortcut, without having to import jQuery. Returns DOM
 * Elements that match the css selector.
 * @param {string} ele The css selector for the element you want returned.
 * @return {Object} The DOM Object, or null if not found.
 */
function $(ele) {
    return document.querySelector(ele);
}

/**
 * A shortcut for css selector, returning an array of matching objects.
 * @param {string} ele the selector for the elements desired.
 * @return {Array} an array of the DOM Objects that match.
 */
function $$(ele) {
    return document.querySelectorAll(ele);
}

(function() {
/** The recorder object */
var recorder;
/** The google profile of the user signed in */
var profile;

/**
 * The main function
 */
window.addEventListener("load", function(){
    // hook all listen events
    var button = $('#MainButton');
    var left = $(".SideButton.left");
    var right = $(".SideButton.right");
    var toggle = $(".switch input");
    // if we're on the main index page with the buttons
    if (button) {
        button.addEventListener("click", buttonToggle);
        left.addEventListener("click", leftToggle);
        right.addEventListener("click", rightToggle);
        toggle.addEventListener("click", onClickMirrorToggle);
    }
    $(".LogoutButton").addEventListener("click", logOut);

    // hook and run the resize function
    window.addEventListener("resize", resize);
    resize();
});

/**
 * returns the value for the cookie named name
 * @param {string} name the Name of the cookie
 * @return The value associated with name
 */
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

/**
 * uploads audio/wav data and spins until returned, displaying results
 * @param {blob} blob The binary audio/wav type data to be uploaded
 */
function upload(blob){
        //var csrftoken = getCookie('csrftoken');
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'upload', true);
        //xhr.setRequestHeader("X-CSRFToken", csrftoken);
        var id_token = getCookie("id_token")

        xhr.onload = function () {
            console.log('DONE', xhr.readyState); // readyState will be 4
            rec_id = parseInt(xhr.response);
            if (isNaN(rec_id)) {
                rec_id = -1
            }
            window.location = "result?rid=" + rec_id;
        };

        xhr.send(blob);

        //Displays the spinner and rotates
        hideButtons();
        var spinner = createSpinner();
        rotate(spinner, 1, 1);
}

/**
 * hides the main 3 ui buttons
 */
function hideButtons() {
    var mainButton = document.getElementById("MainButton");
    mainButton.style.display = 'none';
    var leftButton = document.getElementById("LeftButton");
    leftButton.style.display = 'none';
    var rightButton = document.getElementById("RightButton");
    rightButton.style.display = 'none';
}

/**
 * creates a spinner
 * @return the spinner DOM object
 */
function createSpinner() {
    var spinner = new Image();
    spinner.src = '../../static/spinner.png';
    spinner.id = "spinner";
    $('body').appendChild(spinner);
    return spinner;
}

/* Keeps track of the stream object to stop webcam streaming. */
var localStream;
var mirrorEnabled = false;

/**
 * Requests the user's permission to use camera, if not already attemptd,
 * then attemps to stream a mirrored version of the camera input onto the
 * screen.
 */
function enableMirror() {
    var video = document.querySelector("#videoElement");
    var mirror = document.getElementById("mirrorContainer");
    var toggle = $(".switch input");

    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;
     
    if (navigator.getUserMedia) {       
        navigator.getUserMedia({video: true}, handleVideo, videoError);
    }
     
    function handleVideo(stream) {
        // Successfully got the camera stream -- play it in a video on the page!
        video.src = window.URL.createObjectURL(stream);
        localStream = stream;
        mirror.style.display = 'block';
        toggle.checked = true;

        // Adjust the position and size of the "Record" button.
        mirrorEnabled = true;
        resize();
    }
     
    function videoError(e) {
        // Usually occurs because the user denied camera permissions.
        showToast();
        disableMirror();
    }
}

/**
 * Disables the mirror by stopping the camera video stream and hiding
 * the container for the mirror.
 */
function disableMirror() {
    var mirror = document.getElementById("mirrorContainer");
    var toggle = $(".switch input");

    if (localStream != null)
        localStream.stop();

    mirror.style.display = 'none';
    toggle.checked = false;

    // Adjust the position and size of the "Record" button.
    mirrorEnabled = false;
    resize();
}

/**
 * Shows a toast message defined in this page's html for 3 seconds.
 */
function showToast() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");

    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

/**
 * Handles when the user clicks on the mirror toggle. Either enables
 * the mirror or disables the mirror based on the toggle state.
 */
function onClickMirrorToggle() {
    var toggle = $(".switch input");

    if (toggle.checked == true) {
        enableMirror();
    }
    else {
        disableMirror();
    }
}

/**
 * rotates an element
 * @param {object} elem the DOM Object to spin
 * @param {number} speed the refresh rate of the spinner
 * @param {number} degrees the number of degrees to rotate the spinner
 */
function rotate(elem, speed, degrees)
{
	if(elem == null) {
	    return;
	}
	if(navigator.userAgent.match("Chrome")){
		elem.style.WebkitTransform = "rotate("+degrees+"deg)";
	} else if(navigator.userAgent.match("Firefox")){
		elem.style.MozTransform = "rotate("+degrees+"deg)";
	} else if(navigator.userAgent.match("MSIE")){
		elem.style.msTransform = "rotate("+degrees+"deg)";
	} else if(navigator.userAgent.match("Opera")){
		elem.style.OTransform = "rotate("+degrees+"deg)";
	} else {
		elem.style.transform = "rotate("+degrees+"deg)";
	}
	degrees++;
	if(degrees > 359){
		degrees = 0;
	}
	looper = setTimeout(function() { rotate(elem, speed, degrees); },speed);
}

// temporary
var timeInterval = 60 * 60 * 1000;

/**
 * event function for UI to start recording
 * @param {object} button the DOM object for the main center button
 * @param {object} right the DOM object for the right button
 */
function onStart(button, right) {
	button.innerHTML = "STOP";
	right.classList.remove("hide");
	right.classList.remove("SideRedButton");
	right.innerHTML = "PAUSE";
}

/**
 * event function for UI to pause
 * @param {object} button the DOM object for the main center button
 * @param {object} left the DOM object for the left button
 * @param {object} right the DOM object for the right button.
 */
function onPause(button, left, right) {
	button.innerHTML = "RESUME";
	left.classList.remove("hide");
	left.innerHTML = "RESTART";
	right.innerHTML = "STOP";
	right.classList.add("SideRedButton");
}

/**
 * event function for UI to resume recording
 * @param {object} button the DOM object for the main center button
 * @param {object} left the DOM object for the left button
 * @param {object} right the DOM object for the right button.
 */
function onResume(button, left, right) {
	button.innerHTML = "STOP";
	left.classList.add("hide");
	right.innerHTML = "PAUSE";
	right.classList.remove("SideRedButton");
}

/**
 * event function for UI to stop recording
 * @param {object} button the DOM object for the main center button
 * @param {object} left the DOM object for the left button
 * @param {object} right the DOM object for the right button.
 */
function onStop(button, left, right) {
	button.innerHTML = "RECORD";
	left.classList.add("hide");
	right.classList.add("hide");
	// window.location = "result";
    disableMirror(); 
}

/**
 * event function for UI to reset the buttons
 * @param {object} button the DOM object for the main center button
 * @param {object} left the DOM object for the left button
 * @param {object} right the DOM object for the right button.
 */
function onRestart(button, left, right) {
	button.innerHTML = "RECORD";
	left.classList.add("hide");
	right.classList.add("hide");
	right.classList.remove("SideRedButton");
}

/**
 * event function for when the main center button is clicked
 */
function buttonToggle(e) {
	var button = $("#MainButton");
	var left = $(".SideButton.left");
	var right = $(".SideButton.right");
	if (recorder == null) {
		newRecorder().then(function(record) {
		recorder = record;
		recorder.start(timeInterval);
		onStart(button, right);
		});
	} else {
		switch (button.innerHTML) {
			case "RECORD":
				recorder.start(timeInterval);
				onStart(button, right);
				break;
			case "STOP":
				recorder.stop();
				onStop(button, left, right);
				break;
			case "RESUME":
				recorder.resume();
				onResume(button, left, right);
				break;
		}
	}
}

/**
 * event function for when the left button is clicked
 */
function leftToggle(e) {
	var button = $("#MainButton");
	var left = $(".SideButton.left");
	var right = $(".SideButton.right");
	if (recorder != null) {
		newRecorder().then(function(record) {
			recorder.stop();
			recorder = record;
		});
		onRestart(button, left, right);
	}
}

/**
 * event function for when the right button is clicked
 */
function rightToggle(e) {
	var button = $("#MainButton");
	var left = $(".SideButton.left");
	var right = $(".SideButton.right");
	if (recorder != null) {
		switch (right.innerHTML) {
			case "PAUSE":
				recorder.pause();
				onPause(button, left, right);
				break;
			case "STOP":
				recorder.resume();
				recorder.stop();
				onStop(button, left, right);
				break;
		}
	}
}

/**
 * Called when the user clicks the "Log Out" button.
 * Signs the user out and enbales the "Sign In" button.
 */
function logOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
    var buttonLogin = $(".g-signin2");
    buttonLogin.style.display = "block";

    var buttonLogout = $(".LogoutButton");
    buttonLogout.style.display = "none";

    document.cookie = "id_token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;"
    location.reload();
}

/**
 * creates a new recorder object
 * @return a promise to the recorder object
 */
function newRecorder() {
	return new Promise(function(resolve, reject) {
		navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(function(mediaStream) {
		var r = new MediaStreamRecorder(mediaStream);
		r.mimeType = 'audio/wav';
		r.ondataavailable = function(blob) {
		    upload(blob);
		};
		resolve(r);
		}).catch(function(err) {
		reject(err);
		});
	});
}

/**
 * Event function for the UI to resize according to the screens max width/height
 */
function resize(e) {
    var w = window.innerWidth;
    if (mirrorEnabled == true) {
        w /= 4;
    }
    var h = window.innerHeight;
    var s = (w > h ? h : w);

    var mirrorLeftMargin = w * 2.8;

    // main button
    var button = $("#MainButton");
    if (button) {
        var buttonScale = s * 2 / 3;
        button.style.width = buttonScale + "px";
        button.style.height = buttonScale + "px";
        button.style.borderWidth = s * 0.015 + "px";
        button.style.fontSize = s * 1 / 6 + "px";
        button.style.lineHeight = buttonScale + "px";
        var heightMargin = (h - buttonScale ) * (1 / 2 - 0.03);
        var widthMargin = (w - buttonScale ) * (1 / 2 - 0.03);
        button.style.top = Math.round(heightMargin) + "px";
        if (mirrorEnabled == true) {
            button.style.left = mirrorLeftMargin + "px";
        }
        else {
            button.style.left = Math.round(widthMargin) + "px";    
        }

        // secondary buttons
        var smallButtonScale = s * 1 / 4;
        $$(".SideButton").forEach(function(ele) {
            ele.style.width = smallButtonScale + "px";
            ele.style.height = smallButtonScale + "px";
            ele.style.lineHeight = smallButtonScale + "px";
            ele.style.fontSize = s * 1 / 16 + "px";
            ele.style.top = Math.round(heightMargin
                + buttonScale - smallButtonScale) + "px";
        });
        var leftButton = $(".SideButton.left");
        var rightButton = $(".SideButton.right");
        var circleOffset = 0;
        if (mirrorEnabled == true) {
            leftButton.style.left = mirrorLeftMargin - smallButtonScale + circleOffset + "px";
            rightButton.style.left = mirrorLeftMargin + buttonScale - circleOffset + "px";
        }
        else {
            leftButton.style.left = Math.round(
                widthMargin - smallButtonScale + circleOffset) + "px";
            rightButton.style.left = Math.round(
                widthMargin  + buttonScale - circleOffset) + "px";
        }
    }   
}
})();

/**
 * @param  {googleUser} Represents the Google User.
 */
function onSignIn(googleUser) {
    profile = googleUser.getBasicProfile();
    //console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    //console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail());
    var id_token = googleUser.getAuthResponse().id_token;
    //console.log('ID Token: ' + id_token);

    var buttonLogin = $(".g-signin2");
    buttonLogin.style.display = "none";

    var buttonLogout = $(".LogoutButton");
    buttonLogout.style.display = "block";

    var userName = document.getElementById("UserName");

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'login', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    if (document.cookie.indexOf('id_token') == -1) {
        document.cookie = "id_token=" + id_token;
        xhr.send();
        location.reload();
    } else {
        document.cookie = "id_token=" + id_token;
        xhr.send();
    }

    // This code is sends the user's token to our backend.
    /*
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://yourbackend.example.com/tokensignin');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log('Signed in as: ' + xhr.responseText);
        };
    xhr.send('idtoken=' + id_token);
    */
}
