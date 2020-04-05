from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import psycopg2
import os

app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser='', # removed credentials
    dbpass='',
    dbhost='',
    dbname=''
    )
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1234'

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes
from app.models import User, Employee

@login.user_loader
def load_user(o_id):
    u = User.query.get(int(o_id))
    return u
