import cv2
import numpy as np
import os
import mysql.connector
from datetime import datetime
import getpass          # para digitar senha “oculta” no console (opcional)

# ---------- Configurações ----------
PASTA_ROSTOS  = "rosto"
os.makedirs(PASTA_ROSTOS, exist_ok=True)

DB_HOST       = "localhost"
DB_USER       = "root"
DB_PASSWORD   = "11010412@Pao"
DB_NAME       = "star_gate"
TABELA_FUNCIONARIOS = "funcionarios"

# ---------- Inicializa o classificador antes das funções ----------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------- Utilidades ----------
def conectar_banco():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            auth_plugin="mysql_native_password"
        )
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None


def carregar_rostos_disco():
    dados, nomes = [], []
    for arquivo in os.listdir(PASTA_ROSTOS):
        caminho  = os.path.join(PASTA_ROSTOS, arquivo)
        img_gray = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
        if img_gray is None:
            continue
        for (x, y, w, h) in face_cascade.detectMultiScale(img_gray, 1.1, 5):
            rosto = cv2.resize(img_gray[y:y + h, x:x + w], (100, 100))
            dados.append(rosto.flatten())
            nomes.append(os.path.splitext(arquivo)[0])
    return np.array(dados), nomes


def cadastrar_rosto(gray, nomes_existentes):
    rostos = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(rostos) == 0:
        print("Nenhum rosto detectado. Tente novamente.")
        return False

    # ---------- perguntas ----------
    nome  = input("Nome completo: ").strip()
    cpf   = input("CPF (somente números): ").strip()
    email = input("Email: ").strip()
    cargos = input("Cargo(s): ").strip()
  
   # em produção, faça hashing!

    if nome in nomes_existentes:
        print("Já existe um rosto cadastrado com esse nome.")
        return False

    mydb = conectar_banco()
    if not mydb:
        return False
    cur = mydb.cursor()

    for (x, y, w, h) in rostos:
        # ----- salva local -----
        caminho_local = os.path.join(PASTA_ROSTOS, f"{nome}.jpg")
        cv2.imwrite(caminho_local, rosto_resized)
        print(f"Rosto de {nome} salvo em {caminho_local}")

        # ----- salva no banco -----
        _, buf = cv2.imencode(".jpg", rosto_resized)
        try:
            cur.execute(
                f"""
                INSERT INTO {TABELA_FUNCIONARIOS}
                (Nomes, Email, CPF, Cargos, Rostos, Horario)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (nome, email, cpf, cargos, buf.tobytes(), datetime.now())
            )
            mydb.commit()
            print("Registro inserido no MySQL com sucesso!")
        except mysql.connector.Error as err:
            print(f"Falha ao inserir no banco: {err}")
            mydb.rollback()
            cur.close()
            mydb.close()
            return False

    cur.close()
    mydb.close()
    return True


# ---------- Execução ----------
print("Pressione 'c' para cadastrar novo rosto, 'q' para sair.")

X_train, nomes_salvos = carregar_rostos_disco()   # carrega uma vez
cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in rostos:
        rosto_flat = cv2.resize(gray[y:y + h, x:x + w], (100, 100)).flatten()
        nome_rec   = "Desconhecido"

        if len(X_train) > 0:
            dist = np.linalg.norm(X_train - rosto_flat, axis=1)
            idx  = np.argmin(dist)
            if dist[idx] < 3000:                        # threshold empírico
                nome_rec = nomes_salvos[idx]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, nome_rec, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 0), 2)

    cv2.imshow("Reconhecimento Facial", frame)
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q") or tecla == ord("Q"):
        break
    elif tecla == ord("c") or tecla == ord("C"):
        if cadastrar_rosto(gray, nomes_salvos):
            X_train, nomes_salvos = carregar_rostos_disco()  # recarrega após novo cadastro

cap.release()
cv2.destroyAllWindows()
