/**
 * shortcut for css selector of a dom element
 * @param {string} ele the css selector of the element
 * @return the first matching element
 */
function $(ele) {
  return document.querySelector(ele);
} 

/**
 * the main function
 */
window.addEventListener("load", function(e) {
  var menubutton = $("#MenuButton");
  if (menubutton) {
    menubutton.addEventListener('click', function(e){
        menubutton.classList.toggle('open');
        $("#Sidebar").classList.toggle('open');
        window.addEventListener("resize", resizeSideBar);
        resizeSideBar();
    });
  }
});

/**
 * event function to handle sidebar screen resizing.
 */
function resizeSideBar(e) {
  var w = window.innerWidth;
  var h = window.innerHeight;
  var s = (w > h ? h : w);
  // side bar height
  $("#Sidebar").style.height = h + "px";
}
