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
from studyonline.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from studyonline.main.routes import main
    from studyonline.users.routes import users
    from studyonline.rooms.routes import rooms
    from studyonline.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(rooms)
    app.register_blueprint(errors)

    return app