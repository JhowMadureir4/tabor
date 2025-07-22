from flask_login import UserMixin
from datetime import datetime
from . import db

# Modelo de usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    tabor_feito = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200))  # caminho para a imagem
    is_admin = db.Column(db.Boolean, default=False)

    presencas = db.relationship('Presenca', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

# Modelo de reunião
class Reuniao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    tema = db.Column(db.String(200), nullable=False)

    presencas = db.relationship('Presenca', backref='reuniao', lazy=True)

    def __repr__(self):
        return f'<Reuniao {self.data} - {self.tema}>'

# Modelo de presença
class Presenca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reuniao_id = db.Column(db.Integer, db.ForeignKey('reuniao.id'), nullable=False)
    data_confirmada = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Presenca User:{self.user_id} Reuniao:{self.reuniao_id}>'