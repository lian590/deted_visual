from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
from .. import db
from ..models import Professor

adm = Blueprint('adm', __name__)

@adm.route('/adm')
def adm_dashboard():
    professores = Professor.query.all()
    return render_template('adm.html', dados=professores)
