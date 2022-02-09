from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_wtf import CSRFProtect
# from flask_migrate import Migrate


# csrf = CSRFProtect()
from web import app

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
# migrate = Migrate()
