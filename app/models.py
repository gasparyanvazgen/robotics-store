from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .main import login_manager

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Product id={self.id} name={self.name} price={self.price} \
currency={self.currency} amount={self.amount}>'


class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser id={self.id} username={self.username}'


@login_manager.user_loader
def load_user(user_id):
    # return the user object for the user_id
    return AdminUser.query.get(int(user_id))
