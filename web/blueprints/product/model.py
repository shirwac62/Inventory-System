from flask_login import UserMixin

from web.extensions import db


class Product(UserMixin, db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)

