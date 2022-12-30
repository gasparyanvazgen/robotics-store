from flask import url_for, redirect, flash
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, logout_user

from ..models import Product, db, User

admin = Admin()


class AdminView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        pass


class LogoutView(BaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('main.index'))


admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))
