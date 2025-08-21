# app/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
import os

auth = Blueprint('auth', __name__)

# CONFIG (coloque o db_config de forma adequada ou importe de config.py)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '93845208',
    'database': 'pk'
}

@auth.route('/pos_login')
def pos_login():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM funcionario")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pos_login.html', dados=dados)

@auth.route('/')
def display():
    return render_template('display.html')

@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        rg = request.form['cpf_pk']
        email = request.form['sk_email']
        senha1 = request.form['senha_1']
        senha2 = request.form['senha_2']
        imagem = request.files['image']

        if senha1 != senha2:
            flash('As senhas não coincidem!')
            return redirect(url_for('auth.cadastro'))

        if not rg or not email or not senha1 or not imagem:
            flash('Todos os campos são obrigatórios!')
            return redirect(url_for('auth.cadastro'))

        senha_hash = generate_password_hash(senha1)
        nome_arquivo = secure_filename(imagem.filename)
        caminho = os.path.join('static/imagens', nome_arquivo)
        imagem.save(caminho)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO funcionario(cpf_pk, sk_email, senha, imagem) VALUES (%s, %s, %s, %s)", (rg, email, senha_hash, caminho))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('cadastro2.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cp = request.form['cpf_pk']
        senha = request.form['senha']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionario WHERE cpf_pk = %s", (cp,))
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario['senha'], senha):
            flash('Login realizado com sucesso!')
            return redirect(url_for('auth.pos_login'))
        else:
            flash('Email ou senha incorretos!')
        cursor.close()
        conn.close()
    return render_template('login.html')



