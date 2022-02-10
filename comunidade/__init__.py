
# SQL Alchemy: Banco de dados integrado com Flash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Configurar token de acesso. para maior segurança. Criado Token Padrão (Token criado usando o 'secrets' do Python
app.config['SECRET_KEY'] = 'fd9ba25ecf16ec8eb5f838f230b89eb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.bd'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'manterLogin'
login_manager.login_message_category = 'alert-info'


from comunidade import routes