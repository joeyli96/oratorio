(function() {
  function $(ele) {
    return document.querySelector(ele);
  } 

  window.addEventListener("load", function(e) {
    $('#MenuButton').addEventListener('click', function(e){
        $('#MenuButton').classList.toggle('open');
        $("#Sidebar").classList.toggle('open');
        window.addEventListener("resize", resizeSideBar);
        resizeSideBar();
    });
  });


  function resizeSideBar(e) {
    var w = window.innerWidth;
    var h = window.innerHeight;
    var s = (w > h ? h : w);
    // side bar height
    $("#Sidebar").style.height = h + "px";
  }
})();