from flask_wtf import FlaskForm
# from inventorymanagement import app, mysql, db
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
# from inventorymanagement.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')