from datetime import timedelta

DEBUG = True
LOG_LEVEL = 'DEBUG'
SECRET_KEY = 'abdinafac'

# SQLAlchemy.
db_uri = 'postgresql://postgres:ali12.,ali@127.0.0.1/inv3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = db_uri

# User.
SEED_ADMIN_EMAIL = ""
SEED_ADMIN_PASSWORD = "123bb"
SEED_ADMIN_USER = "adminstrator"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
REMEMBER_COOKIE_DURATION = timedelta(minutes=60)
SESSION_COOKIE_HTTPONLY = True