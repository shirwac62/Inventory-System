from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class AddLocation(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    # name = StringField('Name', [DataRequired(), Length(3, 254)])
    description = StringField('description', [Length(3, 254)])
    rent = IntegerField('kiro')
    submit = SubmitField('Add Location')

