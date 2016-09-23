import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Flask Limiter configs
RATELIMIT_STRATEGY = 'fixed-window'
RATELIMIT_GLOBAL = '2/second,100/minute'