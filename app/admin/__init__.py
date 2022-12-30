from flask_admin import Admin

from .views import IndexView, CustomModelView, UserView, LogoutView
from ..models import Product, db, User

admin = Admin(index_view=IndexView())

admin.add_view(CustomModelView(Product, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))
