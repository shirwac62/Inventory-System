from flask_login import UserMixin
from web.extensions import db


class location(UserMixin, db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    rent = db.Column(db.Integer)

