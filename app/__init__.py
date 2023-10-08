import firebase_admin
from firebase_admin import credentials
from flask import Flask

from app.models import db, User
from config import GOOGLE_APPLICATION_CREDENTIALS, STORAGE_BUCKET
from .admin import admin
from .main import main as main_blueprint, login_manager


def create_app():
    app = Flask(__name__)

    # Load the default configuration
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    # Create the database tables if they don't exist
    with app.app_context():
        db.drop_all()  # drop all tables
        db.create_all()  # create table if not exists

    # blueprints
    app.register_blueprint(main_blueprint)

    cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
    firebase_admin.initialize_app(cred, {
        'storageBucket': STORAGE_BUCKET
    })

    return app
