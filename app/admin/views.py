import os
import secrets

from flask import redirect, url_for, Markup
from flask_admin import BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from wtforms import IntegerField, DecimalField
from wtforms.validators import NumberRange

from config import IMAGE_UPLOADS


# Generates a filename from the model and the loaded file object
def generate_random_image_name(model, file_data):
    random_hex = secrets.token_hex(8)
    return random_hex


class CustomBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CustomModelView(ModelView):
    # Enable data export for the view
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class IndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


class ProductView(CustomModelView):
    # add search field
    column_searchable_list = ['name']

    # set the name of the search field
    column_search_name = 'name'

    # show the description column in the details view
    can_view_details = True
    column_details_list = ['name', 'price', 'amount', 'description', 'image', 'category']

    # hide the description column in the list view
    column_exclude_list = ['description']

    # customize columns for export
    column_export_list = column_details_list

    # pass the _list_thumbnail function to the image_user field
    column_formatters = {
        'image': lambda self, c, m, n: self._list_thumbnail(c, m, n)
    }

    form_extra_fields = {
        'price': DecimalField('Amount', validators=[NumberRange(min=0)]),
        'amount': IntegerField('Amount', validators=[NumberRange(min=0)]),
        'image': ImageUploadField('Upload image',
                                  base_path=IMAGE_UPLOADS,
                                  url_relative_path='img/uploads/',
                                  namegen=generate_random_image_name,
                                  allowed_extensions=['jpg', 'jpeg', 'png'],
                                  max_size=(1000, 1000, False))
    }

    def _list_thumbnail(self, context, model, name):
        # Generate thumbnail image for model object
        url = url_for('static', filename=os.path.join('img/uploads/', model.image))
        return Markup(f'<img src={url} width="100">')

    # Customize the data that is exported for the image and category columns
    def get_export_value(self, model, column):
        # Generate absolute URL with hostname included for image column
        if column == 'image':
            return url_for('static', filename=os.path.join('img/uploads/', model.image), _external=True)

        # Return default value for other columns
        return super(ProductView, self).get_export_value(model, column)


class UserView(CustomModelView):
    def on_model_change(self, view, model, is_created):
        model.password_hash = generate_password_hash(model.password_hash)


class LogoutView(CustomBaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('main.index'))
