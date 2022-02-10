# importando a variável iniciada no MAIN
from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    # get pega direto pelo PK da tabela
    # usar o int() é uma garantia pra pegar ele como integer. não é obrigatório
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    photo = database.Column(database.String, nullable=False, default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    courses = database.Column(database.String, nullable=False, default="Não informado")

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    content = database.Column(database.Text, nullable=False)
    date_creation = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Contato(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    fone = database.Column(database.String, nullable=False)
    mensagem = database.Column(database.Text, nullable=False)