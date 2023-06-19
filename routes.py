from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta

app = Flask(__name__)

lista_usuarios = ['Michele', 'Wallace', 'Murilo', 'Karol']

app.config['SECRET_KEY'] = 'ec3110c1be98aef6ed6acd9976fcedb7'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:    # Verifica se está validado e o botão clicado
        flash(f'Login realizado com sucesso no e-mail: {form_login.email.data}', 'alert-success')    # .data é o que foi preenchido no input de login
        return redirect(url_for('home'))   # Assim que logar será redirecionado para a pagina Home
    return render_template('login.html', form_login=form_login)


@app.route('/criar-conta', methods=['GET', 'POST'])
def criarConta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar-conta.html', form_criarconta = form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)