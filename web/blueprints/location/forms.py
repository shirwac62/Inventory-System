from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class AddLocation(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    description = StringField('description', [Length(3, 254)])
    rent = IntegerField('kiro')
    submit = SubmitField('Add Location')

