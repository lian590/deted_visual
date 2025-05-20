from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector
import time


app = Flask(__name__)
app.secret_key = 'vic_e_lulu'

# Configuração da conexão com o MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '93845208',
    'database': 'pk'
}

@app.route('/pos_login')
def pos_login():
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Consultando os dados
    cursor.execute("SELECT * FROM funcionario") 
    dados = cursor.fetchall()
    
    # Fechando a conexão
    cursor.close()
    conn.close()
    return render_template('pos_login.html', dados=dados)

@app.route('/')
def display():

    return render_template('display.html')




@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        rg = request.form['cpf_pk']
        email = request.form['sk_email']
        senha1 = request.form['senha_1']
        senha2 = request.form['senha_2']
        imagem = request.files['image']

        # Verificação básica
        if senha1 != senha2:
            flash('As senhas não coincidem!')
            return redirect(url_for('cadastro'))

        else:
            flash('Cadastro realizado com sucesso!')
            
        if not rg or not email or not senha1 or not imagem:
            flash('Todos os campos são obrigatórios!')
            

        # Gerar hash da senha
        senha_hash = generate_password_hash(senha1)

        # Salvar imagem com segurança
        nome_arquivo = secure_filename(imagem.filename)
        caminho = os.path.join('static/imagens', nome_arquivo)
        imagem.save(caminho)

        # Aqui você salvaria no banco:
        # salvar_usuario(rg=rg, email=email, senha=senha_hash, imagem=caminho)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO funcionario(cpf_pk, sk_email, senha, imagem) VALUES (%s, %s, %s, %s)", (rg, email, senha_hash, caminho))
        conn.commit()

        # Fechando a conexão
        cursor.close()
        conn.close()

        # R edirecionar ou renderizar uma página de sucesso

        return redirect(url_for('login'))

    return render_template('cadastro2.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cp = request.form['cpf_pk']
        senha = request.form['senha']

        # Conectar ao banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Buscar usuário só pelo e-mail
        cursor.execute("SELECT * FROM funcionario WHERE cpf_pk = %s", (cp,))
        usuario = cursor.fetchone()

        # Verificar senha
        if usuario and check_password_hash(usuario['senha'], senha):
            flash('Login realizado com sucesso!')
            return redirect(url_for('pos_login'))
        else:
            flash('Email ou senha incorretos!')

        # Fechar conexão
        cursor.close()
        conn.close()

    return render_template('login.html')


@app.route('/adm')
def adm():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM professores")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('adm.html')

@app.route('/c')
def funcionarios():
    return render_template('funcionarios.html')

@app.route('/b')
def professores():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM professores")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('professores.html', dados=dados)


@app.route('/a')
def coordenadores():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imagens_salvas")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('coordenadores.html', dados=dados)
if __name__ == '__main__':
    app.run(debug=True)