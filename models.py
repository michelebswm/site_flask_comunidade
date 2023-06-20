from routes import database
from datetime import datetime

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    telefone = database.Column(database.String(14), nullable=True)
    senha = database.Column(database.String(20), nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg', nullable=False)
    posts = database.relationship('Post', backref='autor', lazy=True)      # primeiro parametro 'Post' se refere a classe Post e backre='autor
    cursos = database.Columns(database.String, nullable=False, default='Não Informado')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)   # se refere a classe usuario, coluna id