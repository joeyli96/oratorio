(function() {
    'use strict';

    window.addEventListener("load", function(e) {
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
        var views = document.querySelectorAll(".imageView");
        views.forEach(function(view) {
            var width = parseInt(window.getComputedStyle(view).width);
            var height = width * 9 / 16;
            view.style.height = height + "px";
        })
    }
})();