from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app.models import User
from app.extensions.db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('auth/login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username, password = password).first()
        if user is None:
            flash("Usuario o password incorrecto", "danger")
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('pages.core.home_route'))
    
@auth_bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))