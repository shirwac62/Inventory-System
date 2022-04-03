import click
from sqlalchemy import func, or_
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_utils import database_exists, create_database
from wtforms import form

from web.app import create_app
from web.blueprints.register.models import User
from web.extensions import db

app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


def seed_supper():
    """
    Seed the database with an initial user.
    :return: User instance
    """
    user = User.query.filter(User.username == "SEED_ADMIN_USER").first()
    # user = User.find_by_identity(app.config['SEED_ADMIN_EMAIL'])
    if not user:
        user = User()
        user.email = app.config['SEED_ADMIN_EMAIL']
        user.password = User.encrypt_password(app.config['SEED_ADMIN_PASSWORD'])
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # user.password = app.config['SEED_ADMIN_PASSWORD']
        # user.id = app.config['SEED_ADMIN_USER']
        user.username = app.config['SEED_ADMIN_USER']
        # user.user_type = "superuser"
        user.is_active = True
        user.save_to_db()
    return


@click.command()
def supper():
    return seed_supper()


# if __name__ == '__main__':
#     supper()


cli.add_command(supper)
