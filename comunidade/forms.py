from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user

class FormCriarUsuario(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 25)])
    confirm_password = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo('password')])
    btn_submitCadastroUsuario = SubmitField("Criar Conta")

    # Criar um Validator. A Biblioteca validator roda todas as funções q começam com "validate_"
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Use outro email ou faça login para continuar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Nome de usuário já cadastrado.')




class FormLogin(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    remember_username = BooleanField('Lembrar Usuário')
    btn_submitLoginUsuario = SubmitField("Criar Conta")


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    photo = FileField('Foto de Perfil', validators=[FileAllowed(['jpg','jpeg' ,'png'])])

    curso_python = BooleanField('Curso de Python')
    curso_datamining = BooleanField('Curso de Data Mining')
    curso_SQL = BooleanField('Curso de SQL')

    btn_submitEditarPerfil = SubmitField("Salvar Alteração")

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já cadastrado. Use outro email ou faça login para continuar')

    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError('Nome de usuário já cadastrado.')



class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Conteúdo do Post', validators=[DataRequired()])
    botao_submit = SubmitField('Salvar Post')


class FormContato(FlaskForm):
    nome = StringField("Seu nome: ", validators=[DataRequired(), Length(2,150)])
    email = StringField("Email pra contato: ", validators=[DataRequired(), Email()])
    fone = StringField("Fone/Whatapp pra contato: ", validators=[DataRequired()])
    mensagem = TextAreaField('Digite sua mensagem: ', validators=[DataRequired()])
    botao_submit = SubmitField("Enviar mensagem")
