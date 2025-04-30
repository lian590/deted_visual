const audio = document.getElementById("meuAudio");
const timer = document.getElementById("timer");
let interval;

function tocarAudio() {
    audio.play();
    startTimer();
}

function pausarAudio() {
    audio.pause();
    clearInterval(interval);
}

function reiniciarAudio() {
    audio.currentTime = 0;
    audio.play();
    startTimer();
}

function startTimer() {
    clearInterval(interval);
    interval = setInterval(() => {
        const currentTime = Math.floor(audio.currentTime);
        const minutes = String(Math.floor(currentTime / 60)).padStart(2, '0');
        const seconds = String(currentTime % 60).padStart(2, '0');
        timer.textContent = `${minutes}:${seconds}`;
    }, 1000);
}

audio.addEventListener('ended', () => {
    clearInterval(interval);
    timer.textContent = '00:00'; // Reseta o timer quando o áudio termina
});