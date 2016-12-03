

// It appears that I cannot set cookies in testing.
/*
QUnit.test("getCookie", function(assert) {
	var key = "" + Math.random()
	document.cookie = "cookietest=" + key;
	assert.equal(document.cookie, key, "cookie set incorrectly.");
	var check = getCookie("cookietest");
	document.cookie = null;
	assert.equal(check, key, "getcookie returned incorrect value.");
});
*/

// also disabled because I cannot give permission
/*
QUnit.test("recorder", function(assert) {
	var p = newRecorder()
    p.then(
        function(rec) {
            console.log("Okay.");
        }
    ).catch(
        function(err) {
            assert.notOk(true, "Failed to get permission.");
        }
    );
});
*/

// creates the elements necessary for some tests.

function mainButtons() {
    var container = {};
    var main = document.createElement("div");
    main.id = "MainButton";
    var left = document.createElement("div");
    left.classList.add("SideButton");
    left.classList.add("left");
    var right = document.createElement("div");
    right.classList.add("SideButton");
    right.classList.add("right");
    container.main = main;
    container.left = left;
    container.right = right;
    document.body.appendChild(main);
    document.body.appendChild(left);
    document.body.appendChild(right);
    container.cleanUp = function() {
        main.parentNode.removeChild(main);
        left.parentNode.removeChild(left);
        right.parentNode.removeChild(right);
    }
    return container;
}

function mirror() {
    var container = {};
    var video = document.createElement("video");
    video.id = "videoElement";
    container.video = video;
    var mirror = document.createElement("div");
    mirror.id = "mirrorContainer";
    mirror.appendChild(video);
    container.mirror = mirror;
    var swit = document.createElement("div");
    swit.classList.add("switch");
    var input = document.createElement("input");
    input.type = "checkbox";
    swit.appendChild(input);
    document.body.appendChild(mirror);
    document.body.appendChild(swit);
    container.swh = swit;
    container.cleanUp = function() {
        mirror.parentNode.removeChild(mirror);
        swit.parentNode.removeChild(swit);
    }
    return container;
}

function clearAll(ele) {
    document.querySelectorAll(ele).forEach(function(ele) {
        ele.parentNode.removeChild(ele);
    });
}

/** EVENT TESTS */
QUnit.test("Start Event", function(assert) {
    var c = mainButtons();
    var main = c.main;
    var right = c.right;
    var cl = right.classList;
    cl.add("other");
    cl.add("hide");
    cl.add("SideRedButton");
    onStart(main, right);
    assert.equal(main.innerHTML, "STOP", "Didn't change button to stop.");
    assert.equal(right.innerHTML, "PAUSE", "Didn't change button to pause.");
    assert.ok(cl.contains("other"), "Removed other class styles.");
    assert.notOk(cl.contains("hide"), "Side button hidden.");
    assert.notOk(cl.contains("SideRedButton"), "Side button still red.");
    c.cleanUp();
});

QUnit.test("Pause Event", function(assert) {
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    var cl = left.classList;
    cl.add("hide");
    cl.add("other");
    onPause(main, left, right);
    assert.equal(main.innerHTML, "RESUME", "Didn't change button to resume.");
    assert.equal(right.innerHTML, "STOP", "Didn't change button to stop.");
    assert.equal(left.innerHTML, "RESTART", "Didn't change button to restart.");
    assert.ok(cl.contains("other"), "Left removed extra classes.");
    assert.notOk(cl.contains("hide"), "Left still hidden.");
    c.cleanUp();
});

QUnit.test("Resume Event", function (assert) {
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    var cl = right.classList;
    cl.add("other");
    cl.add("SideRedButton");
    onResume(main, left, right);
    assert.equal(main.innerHTML, "STOP", "Didn't change button to stop");
    assert.equal(right.innerHTML, "PAUSE", "Didn't change right button to pause.");
    assert.ok(left.classList.contains("hide"), "Left button didn't disappear.");
    assert.notOk(cl.contains("SideRedButton"), "Right button still red.");
    assert.ok(cl.contains("other"), "Right button removed other classes.");
    c.cleanUp();
});

QUnit.test("Stop Event UI", function(assert) {
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    // the mirror will be tested seperately...
    var disableMirrorSave = disableMirror;
    disableMirror = function() {};
    onStop(main, left, right);
    disableMirror = disableMirrorSave;
    assert.equal(main.innerHTML, "RECORD", "Didn't change main button.");
    assert.ok(left.classList.contains("hide"), "Left button still visible.");
    assert.ok(right.classList.contains("hide"), "Right button still visible.");
    c.cleanUp();
});

QUnit.test("Restart Event", function(assert) {
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    right.classList.add("SideRedButton");
    right.classList.add("other");
    onRestart(main, left, right);
    assert.equal(main.innerHTML, "RECORD", "Didn't change main button.");
    assert.ok(left.classList.contains("hide"), "Left button still visible.");
    assert.ok(right.classList.contains("hide"), "Right button still visible.");
    assert.ok(right.classList.contains("other"), "Right button removed other classes.");
    assert.notOk(right.classList.contains("SideRedButton"), "Right button still red.");
    c.cleanUp();
});


QUnit.test("Main Button Toggle", function(assert) {
    // spoof some elements
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    recorder = {}; // we currently can't test recorder construction
    // the recorders state should change every time throughout this.

    // mirror will be tested seperately...
    var disableMirrorSave = disableMirror;
    disableMirror = function() {};
    assert.expect(4);
    var verify = "";
    recorder.start = function() {
        assert.ok(true, "recorder started.");
        verify += "s";
    }
    recorder.stop = function() {
        assert.ok(true, "recorder stopped.");
        verify += "x";
    }
    recorder.resume = function() {
        assert.ok(true, "recorder resuming.");
        verify += "r";
    }
    main.innerHTML = "RECORD";
    buttonToggle();
    main.innerHTML = "RESUME";
    buttonToggle();
    main.innerHTML = "STOP";
    buttonToggle();
    disableMirror = disableMirrorSave;
    c.cleanUp();
    assert.equal(verify, "srx", "Didn't activate the functions in the desired order.");
});

QUnit.test("Left button toggle", function(assert) {
    // spoof some elements
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;

    assert.expect(1);

    onRestart = function(a, b, c) {
        assert.ok("restart called.");
    }

    newRecorder = function() {
        return new Promise(function(resolve, reject) {
            reject();
        });
    }

    leftToggle();

    c.cleanUp();
});

QUnit.test("Right button toggle", function(assert) {
    // spoof some elements
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;

    assert.expect(5);

    var verify = "";

    recorder = new function() {
        this.pause = function() {
            assert.ok("paused.");
            verify += "p";
        };
        this.resume = function() {};
        this.stop = function() {
            assert.ok("stopped.");
            verify += "s";
        };
    }

    onPause = function(a, b, c) {
        assert.ok("pause event.");
        verify += "p";
    }

    onStop = function(a, b, c) {
        assert.ok("stop event.");
        verify += "s";
    }

    right.innerHTML = "PAUSE";

    rightToggle();

    right.innerHTML = "STOP";

    rightToggle();

    assert.equal(verify, "ppss");


    recorder = null;

    c.cleanUp();
});

QUnit.test("Sidebar resize", function(assert) {
    var sidebar = document.createElement("div");
    sidebar.id = "Sidebar";
    sidebar.style.height = "100px";
    document.body.appendChild(sidebar);
    window.innerHeight = 300;
    resizeSideBar();
    assert.equal(sidebar.style.height, "300px", "sidebar does not resize.");
    sidebar.parentNode.removeChild(sidebar);
});

QUnit.test("word frequency save", function(assert) {
    clearAll("#transcript");
    var trans = document.createElement("div");
    trans.id = "transcript";
    document.body.appendChild(trans);
    var key = "" + Math.random();
    trans.innerHTML = key;
    saveAndRestore();
    trans.innerHTML = Math.random();
    saveAndRestore();
    assert.equal(trans.innerHTML, key, "transcript not reset.");
    trans.parentNode.removeChild(trans);
});

QUnit.test("word frequency isolates words", function(assert) {
    clearAll("#transcript");
    var trans = document.createElement("div");
    trans.id = "transcript";
    var par = document.createElement("p");
    par.innerHTML = "we're going to select the word batman";
    trans.appendChild(par);
    document.body.appendChild(trans);
    $$ = function() {return [par]};
    wordFrequency("Batman");
    var re = /\<span id\="highlight"\> ?batman ?\<\/span\>/;
    assert.ok(re.test(par.innerHTML), "Did not isolate and corner Batman.");
    trans.parentNode.removeChild(trans);
});

QUnit.test("upload hides button", function(assert) {
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    left.classList.remove("hide");
    right.classList.remove("hide");

    XMLHttpRequest = function() {
        this.open = function(a, b, c) {
        }
        this.addEventListener = function(e, c) {
        }
        this.send = function(b) {
        }
    };

    showToast = function(err) {
        // do nothing.
    }

    upload(null);
    assert.ok(main.classList.contains("hide"));
    assert.ok(left.classList.contains("hide"));
    assert.ok(right.classList.contains("hide"));
    c.cleanUp();
    var spinner = document.getElementById("spinner");
    spinner.parentNode.removeChild(spinner);
});

QUnit.test("upload creates spinner", function(assert) {
    var c = mainButtons();

    showToast = function(err) {
        // do nothing.
    }

    var spinner = document.getElementById("spinner");

    assert.equal(spinner, null);


    XMLHttpRequest = function() {
        this.open = function(a, b, c) {
        }
        this.addEventListener = function(e, c) {
        }
        this.send = function(b) {
        }
    };

    upload(null);



    spinner = document.getElementById("spinner");

    assert.notEqual(spinner, null);

    spinner.parentNode.removeChild(spinner);
    c.cleanUp();
});

QUnit.test("upload uploads", function(assert) {
    var key = "" + Math.random();

    showToast = function(err) {
        // do nothing.
    }

    XMLHttpRequest = function() {
        this.open = function(Param, url, async) {
            assert.equal(Param, "POST");
            assert.equal(url, "upload");
            assert.equal(async, true);
        }
        this.addEventListener = function(event, callback) {
            assert.equal(event.toLowerCase(), "load");
        }
        this.send = function(blob) {
            assert.equal(blob, key);
        }
    }

    var c = mainButtons();

    upload(key);

    var spinner = document.getElementById("spinner");
    spinner.parentNode.removeChild(spinner);
    c.cleanUp();
});


QUnit.test("hideButtons hides button", function(assert) {
    var c = mainButtons();
    var main = c.main;
    var left = c.left;
    var right = c.right;
    left.classList.remove("hide");
    right.classList.remove("hide");

    showToast = function(err) {
        // do nothing.
    }

    hideButtons();

    assert.ok(main.classList.contains("hide"));
    assert.ok(left.classList.contains("hide"));
    assert.ok(right.classList.contains("hide"));
    c.cleanUp();
});

QUnit.test("spinner makes a spinner", function(assert) {
    clearAll("#spinner");
    var s = createSpinner();
    var t = document.getElementById("spinner");
    assert.equal(t.id, "spinner");
    assert.equal(t, s);
    t.parentNode.removeChild(t);
});

QUnit.test("enableMirror ok", function(assert) {
    var m = mirror();

    var key = "" + Math.random();

    window.URL.createObjectURL = function(obj) {
        return key;
    }

    navigator.getUserMedia = function(type, resolve, refuse) {
        assert.ok(type.video);
        assert.notOk(type.audio);
        var stream = {};

        resolve(stream);
        assert.ok(m.video.src.includes(key));
    }

    enableMirror();
    m.cleanUp();
});

QUnit.test("enableMirror notOkay", function(assert) {
    var m = mirror();

    assert.expect(4);

    showToast = function(msg) {
        assert.ok("Showed error");
    }

    disableMirror = function() {
        assert.ok("Disabled mirror!");
    }

    navigator.getUserMedia = function(type, resolve, refuse) {
        assert.ok(type.video);
        assert.notOk(type.audio);
        refuse(null);
    }

    enableMirror();
    m.cleanUp();
});


QUnit.test("disableMirror", function(assert) {
    clearAll(".switch");
    var m = mirror();

    var key = "" + Math.random();

    m.mirror.style.display = key;

    m.swh.checked = true;

    assert.expect(3);

    resize = function() {
        assert.ok("resized");
    }

    localStream = {};

    localStream.stop = function() {
        assert.ok("stream stopped.");
    }

    disableMirror();

    assert.notEqual(m.mirror.style.display, key);

    m.cleanUp();
});

QUnit.test("click Mirror Toggle", function(assert) {
    clearAll(".switch input");
    var m = mirror();

    var toggle = $(".switch input");
    toggle.checked = false;

    var verify = "";

    assert.expect(3);

    disableMirror = function() {
        assert.ok("disabled");
        verify += "d";
    }

    enableMirror = function() {
        assert.ok("enabled.");
        verify += "e";
    }

    onClickMirrorToggle();
    toggle.checked = true;
    onClickMirrorToggle();
    assert.equal(verify, "de");

    m.cleanUp();
});

QUnit.test("showToast", function(assert) {
    var toast = $("#snackbar");

    toast.innerHTML = "";

    var key = "" + Math.random();

    showToast(key);

    assert.equal(toast.innerHTML, key);
    assert.ok(toast.classList.contains("show"));

    setTimeout(function() {
        assert.notOk(toast.classList.contains("show"));
    }, 5500);

});

