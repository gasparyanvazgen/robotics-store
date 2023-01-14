from flask_admin import Admin

from .views import IndexView, CustomModelView, ProductView, UserView, LogoutView
from ..models import db, Product, Category, User

admin = Admin(index_view=IndexView(), template_mode='bootstrap4')

admin.add_view(CustomModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))
