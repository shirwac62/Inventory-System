from datetime import timedelta

DEBUG = True  # False#
LOG_LEVEL = 'DEBUG'  # / CRITICAL / ERROR / WARNING / INFO / DEBUG
# SERVER_NAME = '127.0.0.1:9000'
SECRET_KEY = 'abdinafac'

# SQLAlchemy.
db_uri = 'postgresql://postgres:970894cC@localhost/inventory2'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = db_uri

# # User.
# SEED_ADMIN_EMAIL = 'admin@local.host'
# SEED_ADMIN_PASSWORD = 'aothecode'
# SEED_ADMIN_USER = 'administrator'
# PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
# REMEMBER_COOKIE_DURATION = timedelta(minutes=60)
# SESSION_COOKIE_HTTPONLY = True

