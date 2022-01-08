"""
studyonline package

https://flask-login.readthedocs.io/en/latest/

The login manager contains the code that lets application and Flask-Login work together, 
such as how to load a user from an ID, where to send users when they need to log in
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8447819235'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from studyonline import routes