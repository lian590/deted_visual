from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuração da conexão com o MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '93845208',
    'database': 'ks'
}

@app.route('/pos_login')
def pos_login():
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Consultando os dados
    cursor.execute("SELECT * FROM professores") 
    dados = cursor.fetchall()
    
    # Fechando a conexão
    cursor.close()
    conn.close()
    return render_template('pos_login.html', dados=dados)

@app.route('/')
def display():

    return render_template('display.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
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