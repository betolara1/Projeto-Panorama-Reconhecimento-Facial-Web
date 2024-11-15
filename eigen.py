from database import *
import cv2
import numpy as np
from db import *
from training import *

connection = get_db_connection()
cursor = connection.cursor(dictionary=True)

def gerar_frames():
    # Carregar o reconhecedor
    reconhecedor = cv2.face.EigenFaceRecognizer_create()
    try:
        reconhecedor.read("./lib/classificadorEigen.yml")
    except:
        reconhecedor = treinar_reconhecedor()
        if reconhecedor is None:
            return

    camera = cv2.VideoCapture(0)
    detectorFace = cv2.CascadeClassifier("./lib/haarcascade_frontalface_default.xml")
    reconhecedor = cv2.face.EigenFaceRecognizer_create()
    reconhecedor.read("./lib/classificadorEigen.yml")
    largura, altura = 220, 220
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    id_t = ''
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        imagemCinza = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza, minNeighbors=20, minSize=(30, 30), maxSize=(400, 400))
        for (x,y,l,a) in facesDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y+a,x:x+l],(largura,altura))
            cv2.rectangle(frame,(x,y),(x+l,y+a),(0,0,255),2)
            
            try:
                id_previsto, confianca = reconhecedor.predict(imagemFace)
                id_t = id

                # Buscar nome no banco de dados
                cursor.execute("SELECT nome FROM usuario WHERE cod = %s", (id_previsto,))
                resultado = cursor.fetchone()
                
                if resultado and confianca < 7000:  # Ajuste este valor conforme necessário
                    global nome
                    nome = resultado['nome']
                    cv2.putText(frame, nome, (x, y + a + 30), font, 2, (0, 255, 0), 2)
                    #cv2.putText(frame, f'Conf: {round(confianca)}', (x, y + a + 60), font, 1, (0, 255, 0), 1)
                else:
                    cv2.putText(frame, "Desconhecido", (x, y + a + 30), font, 2, (0, 0, 255), 2)
                
            except Exception as e:
                print(f"Erro no reconhecimento: {str(e)}")
                
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


from datetime import datetime
import csv
from flask import flash

nome_arquivo = 'ponto.csv'
hora = datetime.now()

def gerar_arquivo():
    try:
        if not nome:
            raise ValueError("O nome não pode estar vazio")

        elif nome == 'Desconhecido':
            raise ValueError("O nome não pode estar vazio")
        
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(nome_arquivo, "a+", newline="") as csvfile:
            dados = csv.writer(csvfile)
            tempo = (nome, hora)
            dados.writerow(tempo)

        flash(f"Arquivo gerado com sucesso para {nome}", "success")
        return True

    except ValueError as e:
        flash(f"Erro ao gerar arquivo: {str(e)}", "error")
        return False
    except IOError:
        flash("Erro ao abrir ou escrever no arquivo", "error")
        return False
    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", "error")
        return False
        