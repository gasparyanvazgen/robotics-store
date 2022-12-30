import os
import secrets


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_hex(16)  # generate random key
    MYSQL_USER = os.environ['MYSQL_USER']
    MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
    MYSQL_HOST = os.environ['MYSQL_HOST']
    DATABASE = os.environ['DATABASE']
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{DATABASE}'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://robot:password@localhost:3306/website'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
