import os
import secrets

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


# Generates a filename from the model and the loaded file object
def generate_random_image_name(model, file_data):
    random_hex = secrets.token_hex(8)
    return random_hex


class CustomBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


class CustomModelView(ModelView):
    # Enable data export for the view
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
        # TODO: change the code to properly store the image in firebase
        # Call the parent on_model_change() method to save the model to the database
        super().on_model_change(form, model, is_created)
         # Upload the image to Firebase Storage
        image = form.image.data
        if image:
            # Generate a random filename for the image
            # TODO: that seems to be the problem, i don't need to generate the name again but take the already existing name and use it
            filename = generate_random_image_name(None, image)
             # Create a reference to the Firebase Storage bucket and upload the image
            bucket = firebase_storage.bucket()
            blob = bucket.blob(filename)
             # Set the content type of the image for proper display in Firebase Storage
            blob.content_type = image.content_type
             # Save the image to a local file before uploading
            local_filepath = os.path.join(IMAGE_UPLOADS, filename)
            image.save(local_filepath)
             # Upload the image file to Firebase Storage
            blob.upload_from_filename(local_filepath, content_type=image.content_type)
             # Set the model's image field to the Firebase Storage URL
            model.image = f'https://storage.googleapis.com/{bucket.name}/{filename}'
             # Save the updated model to the database
            # self.session.commit()  # Removed for batch processing
             # Add the model to a batch for batch processing
            self.session.add(model)
             # Remove the local image file after uploading asynchronously
            # delete_local_image_file.delay(local_filepath)

    def _list_thumbnail(self, context, model, name):
        # Use the Firebase Storage URL instead of the local file path
        if model.image:
            return Markup(f'<img src={model.image} width="100">')
        else:
            return Markup(f'<img src={url_for("static", filename="img/default_image.jpg")} width="100">')

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
