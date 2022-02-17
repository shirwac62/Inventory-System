from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class AddMovement(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    from_location = StringField('From Location', [Length(3, 254)])
    to_location = StringField('To Location', [Length(3, 254)])
    quantity = IntegerField('Quantity')
    submit = SubmitField('Add Location')
