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
    user - table
    A user will have [firstname, lastname, email, password] as columns.
    User have relationship with Room table
    backref argument defines a new property on a related model, i.e. Room.
    For example, my_room, an instance of Room model, can access associated user object with expression my_room.user.
    lazy argument tells SQLAlchemy when to load data from a database.
    lazy argument is set to dynamic, which returns a query object, which can be refined further before loading the data.
    By default uselist is True.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), nullable=False)
    username = db.Column(db.String(6), unique=True, nullable=False)
    email = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    rooms = db.relationship('Room', backref='creator', lazy=True)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"       


class Room(db.Model):
    """
    room - table
    A room will have [topic, description]. [id, date_created, user_id] will be populated automatically.
    Room belongs to a user (user_id as foreign key)
    """

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20))
    description = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #members = db.relationship('User') 
    total_members = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"Room('{self.topic}', '{self.date_created}')"