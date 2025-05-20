from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
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






@app.route('/adm')
def adm():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM professores")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('adm.html')
