import cv2
from db import *
from training import *

'''
# --- CONFIGURAÇÃO DA CAMERA --- #
def gen_frames():
    webcam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("./lib/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("./lib/haarcascade_eye.xml")
    
    while True:
        success, frame = webcam.read()
        if not success:
            break
            
        faces = face_cascade.detectMultiScale(frame, minNeighbors=20, minSize=(30, 30), maxSize=(400, 400))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')'''


def gen_frames():
    webcam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("./lib/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("./lib/haarcascade_eye.xml")

    largura, altura = 220, 220

    while True:
        success, video = webcam.read()
        if not success:
            break
            
        imagemCinza = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(video, minNeighbors=20, minSize=(30, 30), maxSize=(400, 400))
        for (x, y, w, h) in faces:
            cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 0), 4)
            region = video[y:y+h, x:x+w]
            eyeCinza = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            eyeDetected = eye_cascade.detectMultiScale(eyeCinza)
            for (ox, oy, ow, oh) in eyeDetected:
                cv2.rectangle(region, (ox, oy), (ox + ow, oy + oh), (0, 255, 0), 2)
            imagemFace = cv2.resize(imagemCinza[y:y + w, x:x + h], (largura, altura))    
        ret, buffer = cv2.imencode('.jpg', video)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
