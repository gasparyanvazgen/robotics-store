from flask_admin import Admin, BaseView, expose
from flask_login import login_required

admin = Admin()


class AdminView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/index.html')


admin.add_view(AdminView(name='Admin View', endpoint='/'))
