from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class SupplierForm(FlaskForm):
    First_Name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    Last_Name = StringField('Last Name', validators=[DataRequired()])
    Address = StringField('Address', validators=[DataRequired()])
    Supplier_Status = StringField('Supplier Status', validators=[DataRequired()])
    Contact_Number = IntegerField('Contact Number', validators=[DataRequired()])
    submit = SubmitField('Add Supplier')
