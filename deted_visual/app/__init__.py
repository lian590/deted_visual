from flask import Flask

app = Flask(__name__)

# Configurações da aplicação podem ser adicionadas aqui

from . import routes  # Importa as rotas definidas em routes.py