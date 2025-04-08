document.getElementById("menu-btn").addEventListener("click", function(){ 
document.getElementById("menu").classList.toggle("active");
});

document.addEventListener("click", function(event) {
    let menu = document.getElementById("menu");
    let menuBtn = document.getElementById("menu-btn");

    if ( !menu.contains(event. target) && event.target !== menuBtn) {
        menu.classList.remove("active");
    }
});





/** 
 * 
*@param {String} page 
* 
*
*
*/
function openFrame (page) {
    fetch(page)
     .then(response => response.text())
     .then(data => {
       document.getElementById("frameContent").innerHTML = data;
       document.getElementById("frameContainer").style.display = "block";
     })
     .catch(error => console.error("erro ao carregar a pagina",
error));
}

function closeFrame() {
   document.getElementById("frameContainer").style.display = "none";
   document.getElementById("frameContent").innertHTML = "";
}