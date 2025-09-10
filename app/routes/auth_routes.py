# app/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from .. import db
from ..models import Funcionario

auth = Blueprint('auth', __name__)

@auth.route('/pos_login')
def pos_login():
    funcionarios = Funcionario.query.all()
    return render_template('pos_login.html', dados=funcionarios)

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
        caminho = os.path.join(current_app.root_path, 'static', 'imagens', nome_arquivo)

        try:
            imagem.save(caminho)
            novo_funcionario = Funcionario(cpf_pk=rg, sk_email=email, senha=senha_hash, imagem=caminho)
            db.session.add(novo_funcionario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao realizar cadastro: {str(e)}')
            return redirect(url_for('auth.cadastro'))

    return render_template('cadastro2.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cp = request.form['cpf_pk']
        senha = request.form['senha']
        usuario = Funcionario.query.filter_by(cpf_pk=cp).first()
        if usuario and check_password_hash(usuario.senha, senha):
            flash('Login realizado com sucesso!')
            return redirect(url_for('auth.pos_login'))
        else:
            flash('CPF ou senha incorretos!')
    return render_template('login.html')



