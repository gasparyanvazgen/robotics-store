import os
import secrets


class Config(object):
    DEBUG = False
    # TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_hex(16)  # generate random key
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://robot:password@localhost:3306/website'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
