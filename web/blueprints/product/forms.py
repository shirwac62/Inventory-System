from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class AddProduct(FlaskForm):
    productname = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])
    location = StringField('Location', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Product')

