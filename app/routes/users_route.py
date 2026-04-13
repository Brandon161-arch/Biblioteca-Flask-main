from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file
from app.models.users import User
from app.models.perfil import Perfil
from app import db
from io import BytesIO
import base64

bp = Blueprint('user', __name__, url_prefix='/user')  # 🔥 MINÚSCULA (IMPORTANTE)

# 🔍 LISTADO DE USUARIOS
@bp.route('/')
def index():
    data = User.query.all()
    return render_template('users/index.html', data=data)

# 📦 API JSON
@bp.route('/js')
def indexjs():
    data = User.query.all()
    result = [user.to_dict() for user in data]
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

# ✏️ EDITAR USUARIO
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.nameUser = request.form['nameUser']
        user.passwordUser = request.form['passwordUser']
        user.email = request.form['email']

        db.session.commit()
        return redirect(url_for('user.index'))

    return render_template('users/edit.html', user=user)

# 👤 DETALLE
@bp.route('/detail/<int:id>')
def detail(id):
    user = User.query.get_or_404(id)
    return render_template('users/detail.html', user=user)

# 🗑️ ELIMINAR
@bp.route('/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user.index'))

# 📱 GENERAR QR (CORREGIDO)
@bp.route('/qr/<int:id>')
def generate_qr(id):
    user = User.query.get_or_404(id)

    qr_base64 = user.generate_qr()
    qr_img = base64.b64decode(qr_base64)

    return send_file(
        BytesIO(qr_img),
        mimetype='image/png'
    )

