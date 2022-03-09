from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class CustomerForm(FlaskForm):
    First_Name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    Last_Name = StringField('Last Name', validators=[DataRequired()])
    Address = StringField('Address', validators=[DataRequired()])
    Contact_Number = IntegerField('Contact Number', validators=[DataRequired()])
    submit = SubmitField('Add Customer')
