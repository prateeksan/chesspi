import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask SQLAlchemy configs
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask Limiter configs
RATELIMIT_STRATEGY = 'fixed-window'
RATELIMIT_GLOBAL = '2/second,100/minute'