const audio = document.getElementById("meuAudio");

function tocarAudio() {
  audio.play();
}

function pausarAudio() {
  audio.pause();
}

function reiniciarAudio() {
  audio.currentTime = 0;
  audio.play();
}