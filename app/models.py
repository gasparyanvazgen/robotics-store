from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product id={self.id} name={self.name} price={self.price} \
currency={self.currency} amount={self.amount}>'


class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<AdminUser id={self.id} username={self.username}'
