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

@app.route('/')
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

@app.route('/c')
def funcionarios():
    return render_template('funcionarios.html')

@app.route('/b')
def professores():
    return render_template('professores.html')

@app.route('/a')
def coordenadores():
    return render_template('coordenadores.html')

if __name__ == '__main__':
    app.run(debug=True)