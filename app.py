from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Rotas HTML
@app.route('/')
def home():
    return render_template("display.html")

@app.route('/login.html')
def login():
    return render_template("login.html")

@app.route('/cadastro.html')
def cadastro():
    return render_template("cadastro.html")

@app.route('/pos_login.html')
def pos():
    return render_template("pos_login.html")

# Pasta de upload
UPLOAD_FOLDER = os.path.join(os.getcwd(), "upload")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Rota para upload da imagem
@app.route('/upload', methods=["GET", "POST"])
def upload_image():
    try:
        data = request.get_json()
        image_data = data.get("image", "")
        
        print("Imagem recebida (início):", image_data[:30])

        if "," in image_data:
            image_base64 = image_data.split(",")[1]
        else:
            return jsonify({'message': 'Formato de imagem inválido'}), 400

        image_bytes = base64.b64decode(image_base64)

        # Gera nome único para a imagem
        filename = f"foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return jsonify({'message': f'Imagem salva com sucesso como {filename}!'})

    except Exception as e:
        print("Erro ao processar imagem:", e)
        return jsonify({'message': 'Erro ao salvar imagem'}), 500

if __name__ == "__main__":
    app.run(debug=True)
