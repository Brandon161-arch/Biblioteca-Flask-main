from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user
from app.models.users import User
from app.models.perfil import Perfil
from app import db
from io import BytesIO
import base64

bp = Blueprint('user', __name__, url_prefix='/user')


# 🔍 LISTADO DE USUARIOS (requiere login)
@bp.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


# 📦 API JSON
@bp.route('/js')
@login_required
def indexjs():
    users = User.query.all()
    result = [user.to_dict() for user in users]
    return jsonify(result)


# ➕ AGREGAR USUARIO
@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']
        email = request.form['email']

        new_user = User(
            nameUser=nameUser,
            passwordUser=passwordUser,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        # 🔥 Crear perfil automáticamente
        new_perfil = Perfil(
            user_id=new_user.idUser,
            bio=''
        )

        db.session.add(new_perfil)
        db.session.commit()

        return redirect(url_for('user.index'))

    return render_template('users/add.html')


# 👤 DETALLE USUARIO
@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    user = User.query.get_or_404(id)
    return render_template('users/detail.html', user=user)


# ✏️ EDITAR USUARIO (SOLO EL DUEÑO)
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)

    # 🔐 SOLO EL DUEÑO
    if user.idUser != current_user.idUser:
        return "No puedes editar este usuario", 403

    if request.method == 'POST':
        user.nameUser = request.form['nameUser']
        user.passwordUser = request.form['passwordUser']
        user.email = request.form['email']

        db.session.commit()
        return redirect(url_for('user.detail', id=user.idUser))

    return render_template('users/edit.html', user=user)


# 🗑️ ELIMINAR USUARIO (SOLO EL DUEÑO)
@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    user = User.query.get_or_404(id)

    # 🔐 SOLO EL DUEÑO
    if user.idUser != current_user.idUser:
        return "No puedes eliminar este usuario", 403

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('auth.logout'))


# 📱 GENERAR QR
@bp.route('/qr/<int:id>')
@login_required
def generate_qr(id):
    user = User.query.get_or_404(id)

    qr_base64 = user.generate_qr()
    qr_img = base64.b64decode(qr_base64)

    return send_file(
        BytesIO(qr_img),
        mimetype='image/png'
    )