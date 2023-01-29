from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user

from .filter import filter_or_search_products
from ..main.forms import LoginForm
from ..models import User, Category

main = Blueprint('main', __name__)

login_manager = LoginManager()
login_manager.login_view = 'main.login'


@main.route('/')
def index():
    page = request.args.get('page', default=None, type=int)
    category_id = request.args.get('category_id', default=0, type=int)
    availability = request.args.get('availability', default=None, type=str)
    search = request.args.get('search', default=None, type=str)

    products, pagination = filter_or_search_products(page, category_id, availability, search)
    categories = Category.query.all()

    return render_template('index.html', categories=categories, products=products, pagination=pagination,
                           page=page, category_id=category_id, availability=availability, search=search)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
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
