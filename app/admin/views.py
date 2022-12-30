from flask import redirect, url_for
from flask_admin import BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash


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


class UserView(CustomModelView):

    # Override the create_model and update_model methods to hash the password
    def create_model(self, form):
        model = self.model()

        # Hash the password before saving it to the database
        form.password_hash.data = generate_password_hash(form.password_hash.data)

        # Save the other form data to the model
        form.populate_obj(model)

        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    def update_model(self, form, model):
        # Hash the password before saving it to the database
        form.password_hash.data = generate_password_hash(form.password_hash.data)

        # Save the other form data to the model
        form.populate_obj(model)

        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()


class LogoutView(CustomBaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('main.index'))
