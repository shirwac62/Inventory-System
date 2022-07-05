from datetime import timedelta

DEBUG = True
LOG_LEVEL = 'DEBUG'
SECRET_KEY = 'abdinafac'

# SQLAlchemy.
# db_uri = 'postgresql://postgres:970894cC@localhost/my-project-inventory2'
db_uri = 'postgres://lowbrbnkjlsldj:faf5e08e0699bb6ef2e69f1b1bbfe455bce2e24e7fb0abcbb1f6f0c85bdb25da@ec2-44-195-162-77.compute-1.amazonaws.com:5432/da9vvo2dg8mj7f?sslmode=require'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = db_uri

# User.
SEED_ADMIN_EMAIL = "adminstrator@gmail.com"
SEED_ADMIN_PASSWORD = "123bb"
SEED_ADMIN_USER = "adminstrator"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
REMEMBER_COOKIE_DURATION = timedelta(minutes=60)
SESSION_COOKIE_HTTPONLY = True