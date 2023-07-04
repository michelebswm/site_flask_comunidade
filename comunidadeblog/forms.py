from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeblog.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(8, 12)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Acessar')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(8, 12)])
    foto_perfil = FileField('Alterar foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_python = BooleanField('Python')
    curso_java = BooleanField('Java')
    curso_springboot = BooleanField('Spring Boot')
    curso_htmlcss = BooleanField('HTML e CSS')
    curso_sql = BooleanField('SQL')
    curso_javascript = BooleanField('JavaScript')
    botao_submit_editarperfil = SubmitField('Salvar Alteração')


    def validate_email(self, email):
        if current_user.email != email.data:    # Só realiza validação se mudar o e-mail
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    btn_submit_criarpost = SubmitField('Criar Post')