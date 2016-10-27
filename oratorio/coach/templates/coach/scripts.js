function $(ele) {
	return document.querySelector(ele);
} 

function $$(ele) {
	return document.querySeletorAll(ele);
}


window.addEventListener("load", function(){
    $('#MenuButton').addEventListener('click', function(e){
	        $('#MenuButton').classList.toggle('open');
			$("#Sidebar").classList.toggle('open');
	});

	window.addEventListener("resize", resize);
	resize();
});

function resize(e) {
	var button = $("#MainButton");
	var w = window.innerWidth;
	var h = window.innerHeight;
	var s = (w > h ? h : w);
	button.style.width = s * 2 / 3 + "px";
	button.style.height = s * 2 / 3 + "px";
	button.style.borderWidth = s * 0.015 + "px";
	button.style.fontSize = s * 1 / 6 + "px";
	button.style.lineHeight = s * 2 / 3 + "px";
	var widthMargin = (w - (s * 2 / 3) ) * (1 / 2 - 0.03);
	var heightMargin = (h - (s * 2 / 3) ) * (1 / 2 - 0.03);
	button.style.top = Math.round(heightMargin) + "px";
	button.style.left = Math.round(widthMargin) + "px";


	$("#Sidebar").style.height = h + "px";
}