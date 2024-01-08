from flask import Flask, redirect, url_for, render_template, session
from rgz import rgz
from flask_sqlalchemy import SQLAlchemy
from Db import db
from Db.models import User, Book
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "123"
user_db = "postgres"
host_ip = "localhost"
host_port = "5432"
database_name = "artur_db"
password = "postgres"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_viev = "rgz.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(rgz)
