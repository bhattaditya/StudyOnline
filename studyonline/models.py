from studyonline import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    returns user object from the user ID stored in the session.
    """

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    table User will be created which will store data in form of objects in Database.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), nullable=False)
    username = db.Column(db.String(6), unique=True, nullable=False)
    email = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    rooms = db.relationship('Room', backref='creator', lazy=True)
    

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

class Room(db.Model):
    """
    table Room will be created which will store data in form of objects in Database.
    """

    id = db.Column(db.Integer, primary_key=True)
    # participants = db.relationship('User', backref='user', lazy=True)
    topic = db.Column(db.String(20))
    description = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # host = user_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # members = db.Column(db.Integer, default=0)
    total_members = db.Column(db.Integer, default=0)
    
    def __repr__(self) -> str:
        return f"Room('{self.topic}', '{self.date_created}')"