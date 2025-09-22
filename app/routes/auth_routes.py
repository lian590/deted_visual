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
        rg = request.form.get('cpf_pk')
        email = request.form.get('sk_email')
        senha1 = request.form.get('senha_1')
        senha2 = request.form.get('senha_2')
        imagem = request.files.get('image')

        if senha1 != senha2:
            flash('As senhas não coincidem!')
            return redirect(url_for('auth.cadastro'))

        if not rg or not email or not senha1:
            flash('CPF, email e senha são obrigatórios!')
            return redirect(url_for('auth.cadastro'))

        # Verificar se o CPF já está cadastrado
        funcionario_existente = Funcionario.query.filter_by(cpf_pk=rg).first()
        if funcionario_existente:
            flash('CPF já cadastrado!')
            return redirect(url_for('auth.cadastro'))

        # Verificar se o email já está cadastrado
        email_existente = Funcionario.query.filter_by(sk_email=email).first()
        if email_existente:
            flash('Email já cadastrado!')
            return redirect(url_for('auth.cadastro'))

        senha_hash = generate_password_hash(senha1)

        # Processar imagem se fornecida (opcional)
        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            # Criar diretório upload se não existir
            upload_dir = os.path.join(current_app.root_path, 'static', 'upload')
            os.makedirs(upload_dir, exist_ok=True)
            caminho = os.path.join(upload_dir, nome_arquivo)

            try:
                imagem.save(caminho)
                print(f"✅ Imagem salva em: {caminho}")
            except Exception as e:
                flash(f'Erro ao salvar imagem: {str(e)}')
                return redirect(url_for('auth.cadastro'))

        try:
            novo_funcionario = Funcionario(cpf_pk=rg, sk_email=email, senha=senha_hash)
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



