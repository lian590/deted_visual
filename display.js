// Pegando o elemento de áudio e o botão
var audio = document.getElementById("meuAudio");
var botao = document.getElementById("botao");  // O ID agora é "botao", como no HTML

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
