import cv2
import sqlite3
import numpy as np
import mediapipe as mp

# Conectar ao banco de dados
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

# Criar a tabela 'faces' se ela não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    face_image BLOB
)
''')
conn.commit()

# Inicializar o MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_ame, cv2.COLOR_BGR2RGB)
    result = mp_face_mesh.process(rgb_frame)
    
    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        face = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in range(468)])
        return face
    return None

# Função para salvar o rosto no banco de dados
def save_face_to_db(face_embedding):
    cursor.execute('INSERT INTO faces (face_image) VALUES (?)', (face_embedding,))
    conn.commit()

# Função para comparar rostos
def compare_faces(face_embedding_1, face_embedding_2):
    # Uma simples comparação de distância
    distance = np.linalg.norm(face_embedding_1 - face_embedding_2)
    return distance

# Função para rastrear rostos e salvar/comparar
def face_tracking():
    cap = cv2.VideoCapture(0)
    face_count = 0
    face_embeddings = []

    while True:
        _, frame = cap.read()
        face_embedding = detect_and_save_face(frame)

        if face_embedding is not None:
            face_embedding = face_embedding.flatten()

            if face_count < 2:
                # Salva os dois primeiros rostos
                save_face_to_db(face_embedding)
                face_embeddings.append(face_embedding)
                face_count += 1
                cv2.putText(frame, f'Rosto {face_count} salvo!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # Compara com os dois primeiros rostos
                distance_1 = compare_faces(face_embedding, face_embeddings[0])
                distance_2 = compare_faces(face_embedding, face_embeddings[1])

                if distance_1 < 0.6:
                    cv2.putText(frame, "Este é o Rosto 1!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                elif distance_2 < 0.6:
                    cv2.putText(frame, "Este é o Rosto 2!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                else:
                    cv2.putText(frame, "Rosto não reconhecido!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Face Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Rodar o rastreamento de rosto
if __name__ == "__main__":
    face_tracking()

    # Fechar a conexão com o banco de dados
    conn.close()
utils

# Função para detectar e salvar rostos
def detect_and_save_face(frame):
    rgb_frame = cv2.cvtColor(fr