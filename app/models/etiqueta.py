from app import db

class Etiqueta(db.Model):

     __tablaname__='etiqueta'
     id=db.Column(db.Integer,primary_key=True)
     nombre=db.Column(db.String(50),nullable=False)
     slug=db.Column(db.String(50),nullable=False)
     