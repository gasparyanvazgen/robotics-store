import os
import secrets
from io import BytesIO

from firebase_admin import storage as firebase_storage
from flask import redirect, url_for, Markup
from flask_admin import BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from wtforms import IntegerField
from wtforms.validators import NumberRange

from config import IMAGE_UPLOADS


# generates a filename from the model and the loaded file object
def generate_random_image_name(model, file_data):
    random_hex = secrets.token_hex(8)
    return random_hex


class CustomBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


class CustomModelView(ModelView):
    # enable data export for the view
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


class IndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


class ProductView(CustomModelView):
    # add search field
    column_searchable_list = ['name']

    # set the name of the search field
    column_search_name = 'name'

    # show the description column in the details view
    can_view_details = True
    column_details_list = ['name', 'price', 'amount', 'description', 'image', 'category']

    # hide the description column in the list view
    column_exclude_list = ['description', 'image']

    # customize columns for export
    column_export_list = column_details_list

    # pass the _list_thumbnail function to the image_user field
    column_formatters = {
        'image': lambda self, c, m, n: self._list_thumbnail(c, m, n)
    }

    form_extra_fields = {
        'price': IntegerField('Price', validators=[NumberRange(min=0)]),
        'amount': IntegerField('Amount', validators=[NumberRange(min=0)]),
        'image': ImageUploadField('Upload image',
                                  base_path=IMAGE_UPLOADS,
                                  url_relative_path='img/uploads/',
                                  namegen=generate_random_image_name,
                                  allowed_extensions=['jpg', 'jpeg', 'png'],
                                  max_size=(1000, 1000, False))
    }

    def on_model_change(self, form, model, is_created):
        # call the parent on_model_change() method to save the model to the database
        super().on_model_change(form, model, is_created)

        # upload the image to Firebase Storage
        image = form.image.data
        if image:
            filename = image.filename  # use the existing image filename
            print(f"filename: {filename}")
            # reference to the Firebase Storage bucket
            bucket = firebase_storage.bucket()

            # create a blob (object) with the same filename in the bucket
            blob = bucket.blob(filename)

            # upload the image file from the local system to Firebase Storage
            blob.upload_from_filename(os.path.join(IMAGE_UPLOADS, filename))

            # make the uploaded blob (image) publicly accessible
            blob.make_public()

            # set the model's image field to the public URL of the uploaded image
            model.image = blob.public_url

            # save the updated model to the database
            self.session.add(model)

    def _list_thumbnail(self, context, model, name):
        # use the Firebase Storage URL instead of the local file path
        if model.image:
            return Markup(f'<img src={model.image} width="100">')
        else:
            return Markup(f'<img src={url_for("static", filename="img/default_image.jpg")} width="100">')

    # customize the data that is exported for the image and category columns
    def get_export_value(self, model, column):
        # generate absolute URL with hostname included for image column
        if column == 'image':
            return url_for('static', filename=os.path.join(IMAGE_UPLOADS, model.image), _external=True)

        # return default value for other columns
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
