import os
import secrets

from flask import redirect, url_for, Markup
from flask_admin import BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from config import IMAGE_UPLOADS


# A function that will generate a filename from the model and the loaded file object.
def generate_random_image_name(model, file_data):
    random_hex = secrets.token_hex(8)
    return random_hex


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


class ProductView(CustomModelView):
    def _list_thumbnail(self, context, model, name):
        url = url_for('static', filename=os.path.join('img/uploads/', model.image))
        return Markup(f'<img src={url} width="100">')

    # pass the _list_thumbnail function to the image_user field
    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'image': ImageUploadField('Upload image',
                                  base_path=IMAGE_UPLOADS,
                                  url_relative_path='img/uploads/',
                                  namegen=generate_random_image_name,
                                  allowed_extensions=['jpg', 'jpeg', 'png'],
                                  max_size=(1200, 780, True))
        # thumbnail_size=(500, 500, True))
    }


class UserView(CustomModelView):
    def on_model_change(self, view, model, is_created):
        model.password_hash = generate_password_hash(model.password_hash)


class LogoutView(CustomBaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('main.index'))
