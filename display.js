// Pegando o elemento de áudio e o botão
var audioElement = document.getElementById("meuAudio");
var playButton = document.getElementById("Ia");  // O ID agora é "botao", como no HTML

// Adicionando evento de clique ao botão
botao.addEventListener("click", function() {
    if (audio.paused) {
        audio.play();
        botao.textContent = "Pausar";
    } else {
        audio.pause();
        botao.textContent = "Tocar";
    }
});
