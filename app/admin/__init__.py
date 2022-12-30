from flask import url_for, redirect, flash
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, logout_user, current_user

from ..models import Product, db, User


class CustomBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        return redirect(url_for('product.index_view'))


class LogoutView(CustomBaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('main.index'))


admin = Admin(index_view=IndexView())

admin.add_view(CustomModelView(Product, db.session))
admin.add_view(CustomModelView(User, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))
