from flask import Flask

from app.models import db
from .admin import admin as admin_blueprint
from .main import main as main_blueprint


def create_app():
    app = Flask(__name__)

    # Load the default configuration
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)

    # Create the database tables if they don't exist
    with app.app_context():
        # db.drop_all()  # drop all tables
        db.create_all()  # create table if not exists

    # blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    return app
