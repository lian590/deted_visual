# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .routes.auth_routes import auth
from .routes.adm import adm

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uma_chave_secreta_qualquer'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(adm)
    return app
