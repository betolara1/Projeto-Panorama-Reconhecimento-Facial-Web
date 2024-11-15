from main import app
from flask import render_template, request, redirect, url_for, Response
from db import *
import detection
import cv2
from datetime import datetime
from eigen import *
from training import *

app.secret_key = 'uma_chave_secreta_muito_segura'

@app.route('/')
def index():
    treinar_reconhecedor()
    return render_template('index.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/captura')
def video_feed():
    return Response(detection.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    cidade = request.form['cidade']

    webcam = cv2.VideoCapture(0)
    success, frame = webcam.read()
    webcam.release()
    
    if success:
        # Converter imagem para JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        foto_bytes = buffer.tobytes()
            

    # Conectar ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir os dados na tabela
    nome_arquivo = f"foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cursor.execute('''
        INSERT INTO usuario (nome, telefone, endereco, cidade, nome_foto, foto, data_captura)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (nome, telefone, endereco, cidade, nome_arquivo, foto_bytes, datetime.now()))

    conn.commit()

    return redirect(url_for('cadastro'))  # Redirecionar de volta para a página inicial



@app.route('/login')
def login():
    treinar_reconhecedor()
    return render_template('login.html')


@app.route('/reconhecimento')
def video_reconhecimento():
    return Response(gerar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/gerar_relatorio')
def gerar_relatorio():
    if gerar_arquivo():
        return redirect(url_for('index'))
    else:
        return redirect(url_for('erro'))


@app.route('/erro')
def erro():
    return render_template('erro.html')