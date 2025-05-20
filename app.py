from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import base64
import os
from datetime import datetime

# Pasta de destino no seu PC (altere esse caminho para onde quiser salvar)
PASTA_PC = "C:/FotosSalvas"

# Cria a pasta "FotosSalvas" se ela não existir
if not os.path.exists(PASTA_PC):
    os.makedirs(PASTA_PC)
    print(f'Pasta criada em: {PASTA_PC}')
else:
    print(f'A pasta já existe: {PASTA_PC}')



#os.makedirs(PASTA_PC, exist_ok=True)#
#Cria a pasta "FotosSalvas" se não existir


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para upload da imagem
@app.route('/upload', methods=["POST"])
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
        destino_pc = os.path.join(PASTA_PC, filename)

        # Salva diretamente na pasta do PC
        with open(destino_pc, "wb") as f:
            f.write(image_bytes)

        return jsonify({'message': f'Imagem salva com sucesso em {destino_pc}!'})

    except Exception as e:
        print("Erro ao processar imagem:", e)
        return jsonify({'message': 'Erro ao salvar imagem'}), 500

if __name__ == '__main__':
    app.run(debug=True)

