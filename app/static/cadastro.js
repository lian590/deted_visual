document.getElementById('startButton').addEventListener('click', function() {
    const video = document.getElementById('video');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
            })
            .catch(function(error) {
                console.error("Erro ao acessar a câmera: ", error);
            });
    } else {
        alert("Seu navegador não suporta acesso à câmera.");
    }
});