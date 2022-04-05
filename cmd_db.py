import click
from web.app import create_app
from web.blueprints.register.models import User
from web.extensions import db, bcrypt

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
    if not user:
        hashed_password = bcrypt.generate_password_hash(app.config['SEED_ADMIN_PASSWORD']).decode('utf-8')
        user = User(username=app.config['SEED_ADMIN_USER'], email=app.config['SEED_ADMIN_EMAIL'],
                    password=hashed_password)
        user.is_active = True
        user.save_to_db()
    return


@click.command()
def supper():
    return seed_supper()


cli.add_command(supper)
