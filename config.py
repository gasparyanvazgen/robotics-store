import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_UPLOADS = os.path.join(BASE_DIR, 'app/static/img/uploads/')
GOOGLE_APPLICATION_CREDENTIALS = 'serviceAccountKey.json'
STORAGE_BUCKET = 'project_id.appspot.com'

PRODUCTS_PER_PAGE = 1


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_hex(16)  # Generate a random key

    # use the PostgreSQL environment variables in the SQLAlchemy URI
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # admin panel credentials
    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
