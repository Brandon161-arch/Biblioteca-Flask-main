from app import db
import re

class Etiqueta(db.Model):
    __tablename__ = 'etiqueta'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, nombre):
        self.nombre = nombre
        self.slug = self.generar_slug(nombre)

    def generar_slug(self, texto):
        return re.sub(r'\s+', '-', texto.lower())