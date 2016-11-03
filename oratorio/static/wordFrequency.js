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
    var line = "";
    var re = /\b/;
    p.innerHTML.split(re).forEach(function(transWord) {
      if (transWord.toLowerCase() == word.toLowerCase()) {
        line += "<span>" + transWord + "</span> ";
      } else {
        line += transWord + " " ;
      }
    });
    p.innerHTML = line.trim();
  });
}

function saveAndRestore() {
  if (savedText.length == 0) {
    savedText = $("#transcript").innerHTML;
  }
  $("#transcript").innerHTML = savedText;
}