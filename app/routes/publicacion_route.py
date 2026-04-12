from flask import Blueprint, render_template
from app.models.publicacion import Publicacion
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.publicacion import Publicacion
from app import db

bp = Blueprint('publicacion',__name__,url_prefix='/publicaciones')
@bp.route('/')
def lista():
    publicaciones = Publicacion.query.all()
    return render_template('publicaciones/lista.html', publicaciones=publicaciones)
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']

        nueva = Publicacion(
            Titulo=titulo,
            contenido=contenido,
            usuario_id=current_user.idUser
        )

        db.session.add(nueva)
        db.session.commit()

        return redirect(url_for('publicacion.lista'))

    return render_template('publicaciones/add.html')