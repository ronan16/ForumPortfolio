# bibliotecas do FLASK:
# Render_template = linkar HTML ao PYTHON
# url_for = permite que os links sejam acessados pela função url_for, evitar link quebrado
# request usado apra pegar a requisição e as informações dela (tipo quem requsitou)
# flash mostra mensagens de alerta
# redirect para redirecionar a para a página destino
import secrets
import os

from flask import render_template, redirect, url_for, request, flash, abort
from comunidade import app, database, bcrypt
from comunidade.forms import FormCriarUsuario, FormLogin, FormEditarPerfil, FormCriarPost, FormContato
from comunidade.models import Usuario, Post, Contato
from flask_login import login_user, logout_user, current_user, login_required

from PIL import Image




# o @app.router é um Decorator, ou seja, uma função da instância do Flask que atribui uma função a um método
@app.route("/")
def home():
    posts = Post.query.order_by(Post.date_creation.desc())
    return render_template('home.html', posts=posts)


@app.route("/contato",  methods=['GET', 'POST'])
def contato():
    form = FormContato()
    if form.validate_on_submit():
        contato = Contato(nome=form.nome.data, email=form.email.data, fone=form.fone.data, mensagem=form.mensagem.data)
        database.session.add(contato)
        database.session.commit()
        flash("Mensagem enviada com sucesso", 'alert-success')
        return redirect(url_for('home'))

    return render_template('contato.html', form=form)


@app.route("/usuarios")
@login_required
def usuarios():
    lista = Usuario.query.all()
    return render_template('usuarios.html', lista=lista)


@app.route("/manter-login", methods=['GET', 'POST']) # Liberar o metodo POST na ágina q tem FORM
def manterLogin():
    formLogin = FormLogin()
    formCriarUsuario = FormCriarUsuario()

    if formLogin.validate_on_submit() and 'btn_submitLoginUsuario' in request.form:
        # implementar o login
        usuario = Usuario.query.filter_by(username=formLogin.username.data).first()
        #check_password (senha_cript, senha_digitada)
        if usuario and bcrypt.check_password_hash(usuario.password, formLogin.password.data):
            login_user(usuario, remember=formLogin.remember_username.data)
            flash(f'Login feito com sucesso! Usuário: {formLogin.username.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login. Email ou senha incorretos', 'alert-danger')

    if formCriarUsuario.validate_on_submit()  and 'btn_submitCadastroUsuario' in request.form:
        # implementar a lógica de criar um usuário no banco de dados
        passCrypt = bcrypt.generate_password_hash(formCriarUsuario.password.data)
        usuario = Usuario(username=formCriarUsuario.username.data, email=formCriarUsuario.email.data, password=passCrypt)
        database.session.add(usuario)
        database.session.commit()
        flash('Conta criada com sucesso para o usuario: {}'.format(formCriarUsuario.username.data), 'alert-success')
        return redirect(url_for('home'))

    return render_template('manter_login.html', formLogin=formLogin, formCriarUsuario=formCriarUsuario)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout realizado com sucesso', 'alert-warning')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.photo))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(title=form.titulo.data, content=form.corpo.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso", 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)



@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.photo))


    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.photo.data:
            nome_imagem = salvar_imagem(form.photo.data, current_user.photo)
            current_user.photo = nome_imagem

        current_user.courses = atualizar_cursos(form)

        database.session.commit()
        flash('Perfil alterado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        marcar_cursos(form, current_user.courses)


    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


def salvar_imagem(imagem, antiga):
    codigo = secrets.token_hex(8)
    nome, ex  = os.path.splitext(imagem.filename)
    nome_completo = nome+codigo+ex
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_completo)

    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    if antiga != 'default.jpg':
        os.remove(os.path.join(app.root_path, 'static/fotos_perfil', antiga))
    imagem_reduzida.save(caminho_completo)

    return nome_completo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name and campo.data is True:
            lista_cursos.append(campo.label.text)

    if lista_cursos:
        return ';'.join(lista_cursos)
    else:
        return 'Não informado'


def marcar_cursos(form, cursos):
    lista = cursos.split(';')
    for item in lista:
        for campo in form:
            if 'curso_' in campo.name:
                if campo.label.text == item:
                    campo.data = True


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)

    if current_user == post.author:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.title
            form.corpo.data = post.content
        elif form.validate_on_submit():
            post.title = form.titulo.data
            post.content = form.corpo.data
            database.session.commit()
            flash("Post alterado com sucesso", "alert-success")
            return redirect(url_for('home'))



    else:
        form = None

    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash("Post Excluído com sucesso", 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)



