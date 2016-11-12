
/**
 * css selector for the first element.
 * @param {string} ele the css selector for the element
 * @return the first DOM object matching ele
 */
function $(ele) {
  return document.querySelector(ele);
}

/**
 * css selector for all elements.
 * @param {string} ele the css selector for the elements
 * @return an array of all DOM object matching ele
 */
function $$(ele) {
  return document.querySelectorAll(ele);
}

/** a save of the original text */
var savedText = "";

/**
 * Highlights word in DOM element #Transcript's paragraphs
 * @param {string} word the word to highlight in the paragraphs
 */
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

/**
 * saves and restores the paragraphs in dom element #Transcript
 */
function saveAndRestore() {
  if (savedText.length == 0) {
    savedText = $("#transcript").innerHTML;
  }
  $("#transcript").innerHTML = savedText;
}