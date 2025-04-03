document.addEventListener("DOMContentLoaded", function () {
    const audio = document.getElementById("audio");
    const playButton = document.getElementById("playButton");
    const stopButton = document.getElementById("stopButton");
    
    playButton.addEventListener("click", function() {
        audio.play();
    });

    stopButton.addEventListener("click", function() {
        audio.pause();
        audio.currentTime = 0;
    });
});