from flask_login import UserMixin
from app import db
import qrcode
from io import BytesIO
import base64
from PIL import Image
import os
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    idUser = db.Column(db.Integer, primary_key=True)
    nameUser = db.Column(db.String(80), unique=True, nullable=False)
    passwordUser = db.Column(db.String(255), nullable=False)  # más espacio para hash
    email = db.Column(db.String(120), unique=True, nullable=False)
    perfil = db.relationship('Perfil', back_populates='user', uselist=False)
    publicaciones = db.relationship('Publicacion', back_populates='usuario')

    # 🔑 Flask-Login
    def get_id(self):
        return str(self.idUser)

    # 🔐 SETEAR CONTRASEÑA (GUARDAR)
    def set_password(self, password):
        self.passwordUser = generate_password_hash(password)

    # 🔓 VERIFICAR CONTRASEÑA (LOGIN)
    def check_password(self, password):
        return check_password_hash(self.passwordUser, password)

    # ❌ NO DEVOLVER PASSWORD
    def to_dict(self):
        return {
            "idUser": self.idUser,
            "nameUser": self.nameUser,
            "email": self.email,
            "rol": self.rol
        }

    # 💾 GUARDAR
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 📱 GENERAR QR
    def generate_qr(self):
        import json

        user_data = json.dumps({
            'ID': self.idUser,
            'Name': self.nameUser
        })

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(user_data)
        qr.make(fit=True)

        img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')

        # logo
        logo_path = os.path.join(current_app.root_path, 'static', 'img', 'sena.png')
        logo = Image.open(logo_path)

        logo_size = 50
        logo = logo.resize((logo_size, logo_size))

        pos = ((img_qr.size[0] - logo_size) // 2, (img_qr.size[1] - logo_size) // 2)
        img_qr.paste(logo, pos)

        buffered = BytesIO()
        img_qr.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return img_str