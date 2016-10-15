(function() {
    'use strict';

    var drawTimeout = null;

    window.addEventListener("load", function(e) {
        easterEgg();
        loadImages();
        window.addEventListener("resize", resize);
        resize();
    });

    // scans the document for .imageView dims and processes into image viewing
    // objects.
    function loadImages() {
        var views = document.querySelectorAll(".imageView");
        views.forEach(function(view) {
            // get the contents
            var lines = view.innerHTML.split("\n");
            view.innerHTML = "";
            // grabs the images
            var images = [];
            lines.forEach(function(line) {
                if (line.trim() != "") {
                    images.push(line.trim());
                }
            });
            startView(view, images);
        });
    }

    // given a dim and an array of image srcs, starts an image viewer
    function startView(view, images) {
        view.style.backgroundImage = "url("+ images[0] +")";
        var container = document.createElement("div");
        container.classList.add("imageTokenContainer");
        view.appendChild(container);
        images.forEach(function(src, index) {
            var circle = document.createElement("dim");
            circle.classList.add("imageToken");
            if (index == 0) {
                circle.classList.add("selected");
            }
            circle.addEventListener("click", function(e) {
                view.style.backgroundImage = "url(" + src + ")";
                container.childNodes.forEach(function(child) {
                    child.classList.remove("selected");
                });
                circle.classList.add("selected");
            });
            container.appendChild(circle);
        });
    }

    // resizes the height of all imageViews so they retain a 16:9 ratio
    function resize(e) {
        if (drawTimeout != null) {
            clearTimeout(drawTimeout);
        }
        drawTimeout = setTimeout(function(e) {
            drawTimeout = null;
            var views = document.querySelectorAll(".imageView");
            views.forEach(function(view) {
                var width = parseInt(window.getComputedStyle(view).width);
                var height = width * 9 / 16;
                view.style.height = height + "px";
            });
        }, 20);
    };


    // THERE IS ABSOLUTELY NOTHING BELOW THIS COMMENT.

    function easterEgg() {
        var heart = document.querySelector("footer span");
        var flipped = false;
        heart.addEventListener("click", function(e) {
            if (!flipped) {
                flipped = true;
                // do some stufffff
                var audio = document.createElement("audio");
                audio.src = "http://trumpshare.com/stuff/songs/3.wav";
                audio.autoplay = true;
                audio.controls = false;
                audio.loop = false;
                document.body.appendChild(audio);

                document.body.classList.add("bgshake");
                var stuff = document.querySelectorAll("*");
                stuff.forEach(function(thing) {
                    if (thing != null && goodElement(thing)
                    && checkForShakeParent(thing)) {
                        thing.classList.add("shake");
                    }
                });
            }
        });
    }

    function goodElement(ele) {
        var badTags = ["HTML", "HEAD", "BODY", "HEADER", "TITLE", "LINK", "SCRIPT"];
        var badIds = ["wrapper"];
        if (ele.width > 0.5 * window.innerWidth) {
            return false;
        }
        if (ele.classList.contains("imageView")) {
            return false;
        }
        return !badTags.includes(ele.nodeName) && !badIds.includes(ele.id);
    }

    function checkForShakeParent(ele) {
        if (!goodElement(ele.parentNode)) {
            return true;
        } else {
            if (ele.classList.contains("shake")) {
                return false;
            } else {
                return checkForShakeParent(ele.parentNode);
            }
        }
    }
})();