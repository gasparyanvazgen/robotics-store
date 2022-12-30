from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user

from ..main.forms import LoginForm
from ..models import User, Product

main = Blueprint('main', __name__)

login_manager = LoginManager()
login_manager.login_view = 'main.login'


@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # check if the user exists and the provided password is correct, then login
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('admin.index'))

        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    # return the user object for the user_id
    return User.query.get(int(user_id))
