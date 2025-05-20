# app/__init__.py
from flask import Flask
from .routes.auth_routes import auth

def create_app():
    app = Flask(__name__)
    app.secret_key = 'uma_chave_secreta_qualquer'
    app.register_blueprint(auth)
    return app
