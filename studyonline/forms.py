from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from studyonline.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    """
    'login' form 
        Fields
            username
            password
        Button
            signin
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    signin = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    'Registration' form 
        Fields
            username
            email
            password
            confirm_password
        Button
            signup
        Flask Validator - SQLAlchemy error
            validate_username()
            validate_email()
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    signup = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already taken!. Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already taken!. Please choose another one.')

class UpdateAccountForm(FlaskForm):
    """
    'UpdateAccount' form 
        Fields
            username
            email
            picture
        Button
            update
        Flask Validator - SQLAlchemy error
            validate_username()
            validate_email()
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=12)])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile', validators=[FileAllowed(['jpg', 'png'])])
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Already taken!. Please choose another one.')
    
    def validate_email(self, email):
         if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Already taken!. Please choose another one.')


# yesterday

class CreateRoomForm(FlaskForm):
    """
    'CreateRoom' form 
        Fields
            topic
            description
        Button
            create
    """

    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    create = SubmitField('Create Room')

class UpdateRoomForm(FlaskForm):
    """
    'UpdateRoom' form 
        Fields
            topic
            description
        Button
            update
    """

    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    update = SubmitField('Update Room')