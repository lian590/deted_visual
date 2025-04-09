import sqlite3
import numpy as np
import cv2

# Conectar ao banco de dados
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

# Função para recuperar e exibir todas as imagens salvas no banco de dados
def show_all_faces():
    # Recuperar todas as imagens do banco de dados
    cursor.execute('SELECT face_image FROM faces')
    rows = cursor.fetchall()

    # Lista para armazenar as imagens convertidas
    images = []

    # Loop para recuperar e converter todas as imagens do banco de dados
    for row in rows:
        face_blob = row[0]  # Cada linha tem a imagem no índice 0
        
        # Converter o BLOB de volta para uma imagem
        nparr = np.frombuffer(face_blob, np.uint8)
        face_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if face_image is not None:
            # Adicionar a imagem convertida à lista
            images.append(face_image)
        else:
            print("Erro ao decodificar uma imagem do banco de dados.")

    # Verifica se há imagens para exibir
    if images:
        # Concatenar todas as imagens horizontalmente (lado a lado)
        all_faces_image = np.concatenate(images, axis=1)
        # Para concatenar verticalmente (uma em cima da outra), use:
        # all_faces_image = np.concatenate(images, axis=0)

        # Exibir todas as imagens juntas
        cv2.imshow('All Faces', all_faces_image)
        cv2.waitKey(0)  # Espera uma tecla ser pressionada
        cv2.destroyAllWindows()  # Fecha a janela de imagem
    else:
        print("Nenhuma imagem encontrada no banco de dados.")

    # Fechar a conexão com o banco de dados
    conn.close()

# Chama a função para exibir todas as imagens armazenadas
if __name__ == '__main__':
    show_all_faces()
