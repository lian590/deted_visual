navigator.mediaDevices.getUserMedia({ video: true, audio: false })
.then(stream => {
  const video = document.getElementById('video');
  video.srcObject = stream;
})
.catch(error => {
  console.error('Erro ao acessar a webcam:', error);
});

function tirarFoto() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imagemBase64 = canvas.toDataURL('image/png');

  fetch('/upload_foto', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ imagem: imagemBase64 })
  })
  .then(response => response.text())
  .then(data => alert(data))
  .catch(err => console.error('Erro ao enviar imagem:', err));
}