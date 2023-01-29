import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_UPLOADS = os.path.join(BASE_DIR, 'app/static/img/uploads')

PRODUCTS_PER_PAGE = 2


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_hex(16)  # generate random key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
