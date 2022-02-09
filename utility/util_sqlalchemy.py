from datetime import date
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.types import TypeDecorator

from utility.util_security import url_encode
from web.extensions import db
from utility.util_datetime import tzware_datetime


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError('{!r} must be TZ-aware'.format(value))
        return value

    def __repr__(self):
        return 'AwareDateTime()'


def meta_info(column, filter_query=None):
    return {
        "name": column.__dict__["key"],
        "label": column.__dict__["key"].title().replace("_", ""),
        "field_type": column.type.__class__.__name__,
        "filter_query": filter_query,
        "has_filter": True if filter_query else False
    }


def log_form_error(form):
    for fieldName, errorMessages in form.errors.items():
        print(fieldName)
        for err in errorMessages:
            print("fieldName: ", fieldName, " Error: ", err)


class ResourceMixin(object):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    created_on = db.Column(db.TIMESTAMP, default=tzware_datetime)
    updated_on = db.Column(db.TIMESTAMP, default=tzware_datetime, onupdate=tzware_datetime)

    @classmethod
    def sort_by(cls, field, direction):
        """
        Validate the sort field and direction.
        :param field: Field name
        :type field: str
        :param direction: Direction
        :type direction: str
        :return: tuple
        """
        table_name = str(cls.__table__)

        if field not in cls.__table__.columns:
            field = 'created_on'

        if direction not in ('asc', 'desc'):
            direction = 'asc'

        if table_name not in field:
            field = table_name + "." + field

        return field, direction

    @classmethod
    def get_bulk_action_ids(cls, scope, ids, omit_ids=[], query=''):
        """
        Determine which IDs are to be modified.

        :param scope: Affect all or only a subset of items
        :type scope: str
        :param ids: List of ids to be modified
        :type ids: list
        :param omit_ids: Remove 1 or more IDs from the list
        :type omit_ids: list
        :param query: Search query (if applicable)
        :type query: str
        :return: list
        """
        omit_ids = map(str, omit_ids)

        if scope == 'all_search_results':
            # Change the scope to go from selected ids to all search results.
            ids = cls.query.with_entities(cls.id).filter(cls.search(query))

            # SQLAlchemy returns back a list of tuples, we want a list of strs.
            ids = [str(item[0]) for item in ids]

        # Remove 1 or more items from the list, this could be useful in spots
        # where you may want to protect the current user from deleting themself
        # when bulk deleting user accounts.
        if omit_ids:
            ids = [id for id in ids if id not in omit_ids]

        return ids

    @hybrid_property
    def url(self):
        return url_encode(self.id)

    @classmethod
    def bulk_delete(cls, ids):
        """
        Delete 1 or more model instances.

        :param ids: List of ids to be deleted
        :type ids: list
        :return: Number of deleted instances
        """
        delete_count = cls.query.filter(cls.id.in_(ids)).delete(
            synchronize_session=False)
        db.session.commit()

        return delete_count

    def save(self):
        """
        Save a model instance.
        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def submit(self):
        """
        Save a model instance.
        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    """
    before_submit	Called before a document is submitted.
    before_cancel	This is called before a submitted document is cancelled.
    before_update_after_submit	This is called before a submitted document values are updated.
    before_insert	This is called before a document is inserted into the database.
    before_naming	This is called before the name property of the document is set.
    autoname	This is an optional method which is called only when it is defined in the controller at document creation. Use this method to customize how the name property of the document is set.
    validate	Use this method to throw any validation errors and prevent the document from saving.
    before_save	This method is called before the document is saved.
    after_insert	This is called after the document is inserted into the database.
    on_update	This is called when values of an existing document is updated.
    on_submit	This is called when a document is submitted.
    on_update_after_submit	This is called when a submitted document values are updated.
    on_cancel	This is called when a submitted is cancelled.
    on_change	This is called to indicate that a document's values has been changed.
    on_trash	This is called when a document is being deleted.
    after_delete	This is called after a document has been deleted.
    """

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()
