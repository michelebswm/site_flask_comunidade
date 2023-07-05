from flask import render_template, request, flash, redirect, url_for
from comunidadeblog import app, database, bcrypt
from comunidadeblog.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeblog.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    lista_posts = Post.query.all()
    return render_template('home.html', lista_posts=lista_posts)

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:    # Verifica se está validado e o botão clicado
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # Se o usuário existe e a senha está correta, o check_password_hash compara o primeiro parâmetro com o segundo, então o primeiro é o que vem no banco e o segundo é o preenchido no formulário
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)     # Efetivamente faz o login remember se a pessoa marcar para lembrar os dados remember será True senão False
            flash(f'Login realizado com sucesso no e-mail: {form_login.email.data}', 'alert-success')    # .data é o que foi preenchido no input de login
            parametro_next = request.args.get('next')   # Pega o parametro que vem no next
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))   # Assim que logar será redirecionado para a pagina Home
        else:
            flash(f'Falha no Login E-mail ou senha incorretos!', 'alert-danger')
    return render_template('login.html', form_login=form_login, body_class='login-page')


@app.route('/criar-conta', methods=['GET', 'POST'])
def criarConta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # Senha Criptografada
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # Criar o usuário pegando as informações preenchidas no formulario
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, telefone=form_criarconta.telefone.data, senha=senha_cript)
        # Adicionar a sessão e dar commit
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar-conta.html', form_criarconta = form_criarconta)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'alert-success')
    return redirect(url_for('home'))

@app.route('/minhaconta')
@login_required
def minha_conta():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('minhaconta.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit() and 'btn_submit_criarpost' in request.form:
        post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form_criarpost=form_criarpost)


def salvar_imagem(imagem):
    # Adicionar código aleatório no nome da imagem
    codigo = secrets.token_hex()
    nome, extensao = os.path.splitext(imagem.filename)  # Separa o nome e a extensão da imagem.filename
    nome_tratado = nome + codigo + extensao # Concatena os 3 textos.
    # Reduzir o nome da imagem
    tamanho = (400, 400)    # Imagem será salva como 200x200
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # Salvar a imagem na pasta fotos_perfil
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_tratado)
    imagem_reduzida.save(caminho_completo)
    return nome_tratado


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                # Adicionar o texto do campo.label na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/minhaconta/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editarperfil = FormEditarPerfil()
    if form_editarperfil.validate_on_submit() and 'botao_submit_editarperfil' in request.form:
        # Alterando informações do current_user para as informações preenchidas no formulário .data
        current_user.email = form_editarperfil.email.data
        current_user.username = form_editarperfil.username.data
        current_user.telefone = form_editarperfil.telefone.data
        if form_editarperfil.foto_perfil.data:
            nome_arquivo_imagem = salvar_imagem(form_editarperfil.foto_perfil.data)
            current_user.foto_perfil = nome_arquivo_imagem
        current_user.cursos = atualizar_cursos(form_editarperfil)
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('minha_conta'))
    elif request.method == 'GET':        # Preenche os inputs dos formulários com os dados do banco
        form_editarperfil.email.data = current_user.email
        form_editarperfil.username.data = current_user.username
        form_editarperfil.telefone.data = current_user.telefone
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', form_editarperfil=form_editarperfil, foto_perfil=foto_perfil)

