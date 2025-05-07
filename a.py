import cv2
import numpy as np
import os
import mysql.connector
from datetime import datetime

# Pasta para salvar os rostos (localmente)
PASTA_ROSTOS = "rostos"
os.makedirs(PASTA_ROSTOS, exist_ok=True)

# Classificador de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- Configurações do Banco de Dados ---
DB_HOST = "localhost"
DB_USER = "root"  # Substitua pelo seu usuário do MySQL
DB_PASSWORD = "93845208"  # Substitua pela sua senha do MySQL
DB_NAME = "ks"  # Substitua pelo nome do seu banco de dados
TABELA_ROSTOS = "imagens_salvas"

def conectar_banco():
    """Conecta ao banco de dados MySQL."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

# Carregar os rostos salvos (do disco)
def carregar_rostos_disco():
    dados = []
    nomes = []
    for arquivo in os.listdir(PASTA_ROSTOS):
        caminho = os.path.join(PASTA_ROSTOS, arquivo)
        img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        rosto_detectado = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in rosto_detectado:
            rosto = img[y:y+h, x:x+w]
            rosto = cv2.resize(rosto, (100, 100))
            dados.append(rosto.flatten())
            nomes.append(os.path.splitext(arquivo)[0])
    return np.array(dados), nomes

# Função para salvar um rosto da webcam (localmente e no banco)
def cadastrar_rosto(frame, gray):
    rostos = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(rostos) == 0:
        print("Nenhum rosto detectado. Tente de novo.")
        return
    
    nome = input("Digite o nome da pessoa: ").strip()
    idade = input("Digite a idade da pessoa: ").strip()
   
    mydb = conectar_banco()
    if not mydb:
        return
    mycursor = mydb.cursor()

    for (x, y, w, h) in rostos:
        rosto_gray = gray[y:y+h, x:x+w]
        rosto_resized = cv2.resize(rosto_gray, (100, 100))
        caminho_local = os.path.join(PASTA_ROSTOS, f"{nome}.jpg")
        cv2.imwrite(caminho_local, rosto_resized)
        print(f"Rosto de {nome} salvo localmente!")

        # Salvar no banco de dados como BLOB
        _, imagem_codificada = cv2.imencode('.jpg', rosto_resized)
        imagem_bytes = imagem_codificada.tobytes()

        query = f"INSERT INTO {TABELA_ROSTOS} (nome, idade, imagem_bytes) VALUES (%s, %s, %s, %s, %s)"
        values = (nome, idade, imagem_bytes)
        try:
            mycursor.execute(query, values)
            mydb.commit()
            print(f"Rosto de {nome} salvo no banco de dados!")
        except mysql.connector.Error as err:
            print(f"Erro ao salvar rosto no banco de dados: {err}")

    mycursor.close()
    mydb.close()

# Inicializar webcam
cap = cv2.VideoCapture(0)

print("Pressione 'c' para cadastrar novo rosto, 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Carregar rostos salvos do disco para o reconhecimento
    X_train_disco, nomes_disco = carregar_rostos_disco()

    for (x, y, w, h) in rostos:
        rosto_atual = gray[y:y+h, x:x+w]
        rosto_atual_resized = cv2.resize(rosto_atual, (100, 100)).flatten()

        nome_reconhecido = "Desconhecido"
        if len(X_train_disco) > 0:
            distancias = np.linalg.norm(X_train_disco - rosto_atual_resized, axis=1)
            indice = np.argmin(distancias)
            if distancias[indice] < 3000:
                nome_reconhecido = nomes_disco[indice]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, nome_reconhecido, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Reconhecimento Facial", frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q'):
        break
    elif tecla == ord('c'):
        cadastrar_rosto(frame, gray)

cap.release()
cv2.destroyAllWindows() 

