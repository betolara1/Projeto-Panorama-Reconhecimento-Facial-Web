from database import *
import cv2
import numpy as np
from db import *

connection = get_db_connection()
cursor = connection.cursor(dictionary=True)

def treinar_reconhecedor():
    try:
        cursor.execute("SELECT cod, foto FROM usuario")
        fotos = cursor.fetchall()

        if not fotos:
            print("Nenhuma foto encontrada no banco de dados.")
            return None

        faces = []
        ids = []
        
        face_cascade = cv2.CascadeClassifier("./lib/haarcascade_frontalface_default.xml")
        if face_cascade.empty():
            print("Erro: Não foi possível carregar o classificador Haar Cascade.")
            return None
        
        for foto in fotos:
            try:
                # Converter bytes para numpy array
                nparr = np.frombuffer(foto['foto'], np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                
                if img is None:
                    print(f"Erro ao decodificar a imagem para o usuário com cod {foto['cod']}.")
                    continue
                
                # Detectar face na imagem
                faces_detected = face_cascade.detectMultiScale(img, minNeighbors=20, minSize=(30, 30), maxSize=(400, 400))
                
                if len(faces_detected) == 0:
                    print(f"Nenhuma face detectada na foto do usuário com cod {foto['cod']}.")
                    continue
                
                for (x, y, w, h) in faces_detected:
                    face_img = cv2.resize(img[y:y+h, x:x+w], (220, 220))
                    faces.append(face_img)
                    ids.append(foto['cod'])
            
            except Exception as e:
                print(f"Erro ao processar a foto do usuário com cod {foto['cod']}: {str(e)}")
                continue

        if not faces:
            print("Nenhuma face válida encontrada nas fotos.")
            return None

        # Criar e treinar o reconhecedor
        reconhecedor = cv2.face.EigenFaceRecognizer_create()
        reconhecedor.train(faces, np.array(ids))
        
        # Salvar o classificador treinado
        reconhecedor.save("./lib/classificadorEigen.yml")
        print("Reconhecedor treinado e salvo com sucesso.")
        return reconhecedor

    except Exception as e:
        print(f"Erro durante o treinamento do reconhecedor: {str(e)}")
        return None
