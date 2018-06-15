var blockingCounter = 0;
function loading(r,a){
	containerState = document.getElementById("button"+r+a).firstChild.className;
	if (containerState == "container0"){
		document.getElementById("button"+r+a).innerHTML =
				"<div class='container1'><div class='spinner dark'><i></i>  <i></i>  <i></i>  <i></i>  <i></i>  <i></i>	<i></i>  <i></i>  <i></i>  <i></i>  <i></i>  <i></i></div></div>";
	}
	if (containerState == "container1"){
		document.getElementById("button"+r+a).innerHTML =
				"<div class='container0'><div class='spinner light'><i></i>  <i></i>  <i></i>  <i></i>  <i></i>  <i></i>	<i></i>  <i></i>  <i></i>  <i></i>  <i></i>  <i></i></div></div>";
	}
}
function toggle(r,a) {
	blockingCounter++;
	loading(r,a);
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4){
			if (this.status == 200) {
				document.getElementById("button"+r+a).innerHTML =
				this.responseText;
			}
			blockingCounter--;
		}
	};
	xhttp.open("GET", "button/"+r+"/"+a+"/", true);
	xhttp.send();
}
function grid() {
	if (blockingCounter == 0){
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200 && blockingCounter == 0) {
				document.getElementById("grid").innerHTML =
				this.responseText;
				}
			};
		xhttp.open("GET", "grid/", true);
		xhttp.send();
		}
	}
window.setInterval(function(){
	grid()
}, {{ refresh_rate }});