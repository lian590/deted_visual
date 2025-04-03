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

