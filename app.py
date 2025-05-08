from flask import Flask, request, render_template
import base64
import os
from datetime import datetime
app = Flask("__name__")

@app.route("/")
def home():
    return render_template("display.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/cadastro.html")
def cadastro():
    return render_template("cadastro.html")

@app.route("/pos_login.html")
def pos():
    return render_template("pos_login.html")


if __name__ == "__main__":
    app.run(debug=True)

app = Flask(__name__, static_url_path='/static')

app = Flask(__name__)

# Pasta onde salvar as imagens
UPLOAD_FOLDER = '/static/upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_foto', methods=['POST'])
def upload_foto():
    data = request.get_json()
    imagem_base64 = data['imagem'].split(',')[1]  # Remove "data:image/png;base64,"

    # Cria nome único para o arquivo
    nome_arquivo = datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)

    # Salva imagem
    with open(caminho_arquivo, 'wb') as f:
        f.write(base64.b64decode(imagem_base64))

    return f'Imagem salva como {nome_arquivo}'