navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(stream => {
    const video = document.getElementById("video");
    video.srcObject = stream;
  })
  .catch(error => {
    console.error('Erro ao acessar a webcam:', error);
  });

function tirarFoto() {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imagemBase64 = canvas.toDataURL("image/png");

  console.log("Base64 enviada:", imagemBase64.slice(0, 30));

  fetch("http://127.0.0.1:5000/upload", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ image: imagemBase64 })
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message);
  })
  .catch(err => {
    console.error("Erro ao enviar imagem:", err);
  });
}
