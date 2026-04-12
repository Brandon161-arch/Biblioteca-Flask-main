from app import db

publicacion_etiqueta = db.Table('publicacion_etiqueta',
    db.Column('publicacion_id', db.Integer, db.ForeignKey('publicacion.id')),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id')),
)
class Publicacion(db.Model):
    __tablaname__='publicacion'
    id= db.Column(db.Integer, primary_key=True)
    Titulo= db.Column(db.String(200), nullable=False)
    contenido= db.Column(db.Text,nullable=False)

    usuario_id=db.Column(db.Integer,db.ForeignKey('users.idUser'))
    usuario = db.relationship('User', back_populates='publicaciones')
    etiquetas=db.relationship(
        'Etiqueta',
        secondary=publicacion_etiqueta,
        backref='publicaciones'
        
    )