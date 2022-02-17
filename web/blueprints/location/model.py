
# import sqlalchemy
from flask_login import UserMixin
# from sqlalchemy import cast

# from utility.util_default import get_current_user
# from utility.util_sqlalchemy import ResourceMixin
from web.extensions import db


class location(UserMixin, db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    rent = db.Column(db.Integer)

    # owner_id = db.Column(db.String(140), db.ForeignKey('user.id'), default=get_current_user,
    #                      onupdate=get_current_user)
    # owner = db.relationship("User", foreign_keys=[owner_id])
    # modified_by_id = db.Column(db.String(140), db.ForeignKey('user.id'), default=get_current_user,
    #                            onupdate=get_current_user)

    # def __eq__(self, other):
    #     return (isinstance(other, self.__class__)) and (self.name == other.name)
    #
    # def __neq__(self, other):
    #     return self.name != other.name
    #
    # def get_series_type(self):
    #     return self.__series_type__
    #
    # def __repr__(self):
    #     return self.name
    #
    # def __init__(self, **kwargs):
    #     # Call Flask-SQLAlchemy's constructor.
    #     super(Product, self).__init__(**kwargs)
    #
    # @staticmethod
    # def pram_column_size():
    #     return 3
    #
    # @staticmethod
    # def sort_column(index):
    #     if index == 0:
    #         return "id"
    #     elif index == 1:
    #         return "name"
    #     else:
    #         return "created_on"
    #
    # @staticmethod
    # def filter_column(index, search):
    #     if search == '':
    #         return
    #     elif index == 0:
    #         return cast(Product.id, sqlalchemy.String).like("%" + search + "%")
    #     elif index == 1:
    #         return Product.name.ilike("%" + search + "%")
    #     else:
    #         return cast(Product.id, sqlalchemy.String).like("%" + search + "%")
