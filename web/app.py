from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from web.blueprints import tenant_list
from web.blueprints.register.models import User
from web.extensions import db, login_manager


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config['USE_SESSION_FOR_NEXT'] = True
    Bootstrap(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    extensions(app)
    for tenant in tenant_list:
        app.register_blueprint(tenant)

        @app.before_first_request
        def create_tables():
            db.create_all()

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).
    :param app: Flask application instance
    :return: None
    """
    db.app = app
    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager.init_app(app)

    return None