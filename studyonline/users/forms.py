from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField
from studyonline.models import User
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

class LoginForm(FlaskForm):
    """
    'login' form 
        Fields
            username
            password
        Button
            submit
    """

    username = StringField(
                'Username', 
                validators=[
                    DataRequired(),
                    Length(min=5, max=10)
                ]
    )
    password = PasswordField(
                'Password', 
                validators=[
                    DataRequired()
                ]
    )
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    'Registration' form 
        Fields
            username
            email
            password
            confirm_password
        Button
            submit
        Flask Validator - SQLAlchemy error
            validate_username()
            validate_email()
    """
    name = StringField(
            'Name', 
            validators=[
                DataRequired(), 
                Length(min=5, max=20)
            ]
    )
    username = StringField(
            'Username', 
            validators=[
                DataRequired(), 
                Length(min=5, max=10)
            ]
    )
    email = StringField(
            'Email', 
            validators=[
                DataRequired(), 
                Email()
            ]
    )
    password = PasswordField(
            'Password', 
            validators=[
                DataRequired()
            ]
    )
    confirm_password = PasswordField(
            'Confirm Password', 
            validators=[
                DataRequired(), 
                EqualTo('password')
            ]
    )  
    submit = SubmitField('Sign Up')

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
            submit
        Flask Validator - SQLAlchemy error
            validate_username()
            validate_email()
    """
    name = StringField(
            'Name', 
            validators=[
                DataRequired(), 
                Length(min=5, max=12)
            ]
    )
    username = StringField(
            'Username', 
            validators=[
                DataRequired(), 
                Length(min=5, max=10)
            ]
    )
    email = StringField(
            'Email', 
            validators=[
                DataRequired(), 
                Email()
            ]
    )
    picture = FileField(
            'Update Profile', 
            validators=[
                FileAllowed(['jpg', 'png'])
            ]
    )
    submit = SubmitField('Update')

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