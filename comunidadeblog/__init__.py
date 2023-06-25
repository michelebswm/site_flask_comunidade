from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ec3110c1be98aef6ed6acd9976fcedb7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Importando o routes para ser executado e colocar os links no ar
from comunidadeblog import routes