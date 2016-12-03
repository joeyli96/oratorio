

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
    var mirror = document.createElement("div");
    mirror.id = "mirrorContainer";
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
