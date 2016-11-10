function $(ele) {
	return document.querySelector(ele);
} 

function $$(ele) {
	return document.querySelectorAll(ele);
}

var recorder;

window.addEventListener("load", function(){
	$('#MainButton').addEventListener("click", buttonToggle);
	$(".SideButton.left").addEventListener("click", leftToggle);
	$(".SideButton.right").addEventListener("click", rightToggle);

	window.addEventListener("resize", resize);
	resize();
});

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

function upload(blob){
        var csrftoken = getCookie('csrftoken');
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'upload', true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    
        // need to get user id here
        xhr.setRequestHeader("UserHeader", "User ID needed");
    
        // the default type is video/webm, is audio/wav supported?
        // also how to convert the blob to .wav file?
        var file = new File([blob], 'video.webm', {type: 'video/webm', lastModified: Date.now()});
        xhr.send(file);
}

// temporary
var timeInterval = 60 * 1000;

function buttonToggle(e) {
	var button = $("#MainButton");
	if (recorder == null) {
		newRecorder().then(function(record) {
		recorder = record;
		recorder.start(timeInterval);
		});
	} else {
		switch (recorder.state) {
			case "inactive":
				recorder.start(timeInterval);
				break;
			case "recording":
				recorder.stop();
				break;
			case "paused":
				recorder.resume();
				break;
		}
	}
}

function leftToggle(e) {
	var button = $(".SideButton.left");
	if (recorder != null) {
		switch (recorder.state) {
			case "paused":
				// RESTART
				newRecorder().then(function(record) {
					recorder.stop();
					recorder = record;
				});
				break;
		}
	}
}

function rightToggle(e) {
	var button = $(".SideButton.right");
	if (recorder != null) {
		switch (recorder.state) {
			case "recording":
				// PAUSE
				recorder.pause();
				break;
			case "paused":
				// STOP
				recorder.stop();
				break;
		}
	}
}

function newRecorder() {
	return new Promise(function(resolve, reject) {
		navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(function(mediaStream) {
		var r = new MediaRecorder(mediaStream);
		r.ondataavailable = function(e) {
		    upload(e.data);
		};
		    
		var s = $("#MainButton");
		var left = $(".SideButton.left");
		var right = $(".SideButton.right");
		r.addEventListener("pause", function(e) {
			s.innerHTML = "RESUME";
			left.classList.remove("hide");
			left.innerHTML = "RESTART";
			right.innerHTML = "STOP";
			right.classList.add("SideRedButton");
		});
		r.addEventListener("resume", function(e) {
			s.innerHTML = "STOP";
			left.classList.add("hide");
			right.innerHTML = "PAUSE";
			right.classList.remove("SideRedButton");
		});
		r.addEventListener("start", function(e) {
			s.innerHTML = "STOP";
			right.classList.remove("hide");
			right.classList.remove("SideRedButton");
			right.innerHTML = "PAUSE";
		});
		r.addEventListener("stop", function(e) {
			s.innerHTML = "RECORD";
			left.classList.add("hide");
			right.classList.add("hide");
			window.location = "result";
		});
		resolve(r);
		}).catch(function(err) {
		reject(err);
		});
	});
}

function resize(e) {
	var w = window.innerWidth;
	var h = window.innerHeight;
	var s = (w > h ? h : w);

	// main button 
	var button = $("#MainButton");
	var buttonScale = s * 2 / 3;
	button.style.width = buttonScale + "px";
	button.style.height = buttonScale + "px";
	button.style.borderWidth = s * 0.015 + "px";
	button.style.fontSize = s * 1 / 6 + "px";
	button.style.lineHeight = buttonScale + "px";
	var widthMargin = (w - buttonScale ) * (1 / 2 - 0.03);
	var heightMargin = (h - buttonScale ) * (1 / 2 - 0.03);
	button.style.top = Math.round(heightMargin) + "px";
	button.style.left = Math.round(widthMargin) + "px";

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
	leftButton.style.left = Math.round(
		widthMargin - smallButtonScale + circleOffset) + "px";
	rightButton.style.left = Math.round(
		widthMargin  + buttonScale - circleOffset) + "px";
}
