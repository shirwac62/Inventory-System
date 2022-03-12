from flask_login import UserMixin

from web.extensions import db


class Supplier(UserMixin, db.Model):
    Supplier_Id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(20), unique=False, nullable=False)
    Last_Name = db.Column(db.String(120), unique=False, nullable=False)
    Address = db.Column(db.String(120), unique=False, nullable=False)
    Supplier_Status = db.Column(db.String(120), unique=False, nullable=False)
    Contact_Number = db.Column(db.Integer, unique=False, nullable=False)
