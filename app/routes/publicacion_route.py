from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db

from app.models.publicacion import Publicacion
from app.models.etiqueta import Etiqueta

bp = Blueprint('publicacion', __name__, url_prefix='/publicaciones')



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
        etiquetas_texto = request.form['etiquetas']

        nueva = Publicacion(
            Titulo=titulo,
            contenido=contenido,
            usuario_id=current_user.idUser
        )

        db.session.add(nueva)
        db.session.commit()

        # 🟢 etiquetas
        if etiquetas_texto:
            etiquetas_lista = [e.strip() for e in etiquetas_texto.split(",") if e.strip()]

            for nombre in etiquetas_lista:
                etiqueta = Etiqueta.query.filter_by(nombre=nombre).first()

                if not etiqueta:
                    etiqueta = Etiqueta(nombre=nombre)
                    db.session.add(etiqueta)
                    db.session.commit()

                if etiqueta not in nueva.etiquetas:
                    nueva.etiquetas.append(etiqueta)

        db.session.commit()

        return redirect(url_for('publicacion.lista'))

    return render_template('publicaciones/add.html')



@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    pub = Publicacion.query.get_or_404(id)

    
    if pub.usuario_id != current_user.idUser:
        return "No puedes editar esta publicación", 403

    if request.method == 'POST':
        pub.Titulo = request.form['titulo']
        pub.contenido = request.form['contenido']

        db.session.commit()

        return redirect(url_for('publicacion.lista'))

    return render_template('publicaciones/editar.html', pub=pub)

@bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    pub = Publicacion.query.get_or_404(id)

    # 🔐 SOLO EL DUEÑO
    if pub.usuario_id != current_user.idUser:
        return "No puedes eliminar esta publicación", 403

    db.session.delete(pub)
    db.session.commit()

    return redirect(url_for('publicacion.lista'))