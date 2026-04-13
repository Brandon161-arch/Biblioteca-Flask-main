from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.users import User

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']
        
        user = User.query.filter_by(nameUser=nameUser, passwordUser=passwordUser).first()

        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('user.index'))  # 🔥 siempre al buscador
        
        flash('Invalid credentials. Please try again.', 'danger')
    
    # 🔥 si ya está logueado → también al buscador (NO dashboard)
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    return render_template("login.html")


@bp.route('/dashboard')
@login_required
def dashboard():
    return f'Welcome, {current_user.nameUser}! This is your dashboard.'


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/pruebajs')
def pruebajs():
    example_data = {
        'title': 'Bienvenido a Flet',
        'message': 'Este es un mensaje desde Flask.'
    }
    import json
    return json.dumps(example_data)