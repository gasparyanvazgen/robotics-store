from flask import Blueprint, render_template, request
from flask_login import LoginManager

from ..main.forms import LoginForm
from ..models import AdminUser

main = Blueprint('main', __name__)

login_manager = LoginManager()
login_manager.login_view = 'main.login'


@main.route('/')
def index():
    return render_template('index.html')  # products list


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        admin_user = AdminUser.query.filter_by(username=form.username.data).first()
        if admin_user is not None and admin_user.verify_password(form.password.data):

            pass
