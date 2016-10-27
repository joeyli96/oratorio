function $(ele) {
	return document.querySelectorAll(ele);
}

window.addEventListener("load", function(){
    $('#nav-icon3 span').forEach(function(ele) {
    	ele.addEventListener('click', function(e){
	        $('#nav-icon3')[0].classList.toggle('open');
	    });
    });
});