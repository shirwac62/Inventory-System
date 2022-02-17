from flask_login import UserMixin

from web.extensions import db


class Movement(UserMixin, db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    from_location = db.Column(db.String(100))
    to_location = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
