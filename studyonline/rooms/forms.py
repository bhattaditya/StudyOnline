from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreateRoomForm(FlaskForm):
    """
    'CreateRoom' form 
        Fields
            topic
            description
        Button
            submit
    """

    topic = StringField('Topic', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Room')