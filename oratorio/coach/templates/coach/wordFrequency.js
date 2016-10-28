function $(ele) {
  return document.querySelector(ele);
}

function $$(ele) {
  return document.querySelectorAll(ele);
}

var savedText = "";

function wordFrequency(word) {
  saveAndRestore();
  $$("#transcript p").forEach(function(p) {
    p.innerHTML.split(" ").forEach(function(word) {

    });
  });
}

function saveAndRestore() {
  if (savedText.length == 0) {
    savedText = $("#transcript").innerHTML;
  }
  $("#transcript").innerHTML = savedText;
  
}