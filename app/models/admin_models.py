from flask_admin import AdminIndexView, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from app.models.models import User, UsersRoles, Role
from app import db

#db = SQLAlchemy()


# Define the User data model.
class AdmUsers(db.Model):
    def create_adm_user(self):
        return User


class AdmUsersRoles(db.Model):
    def create_adm_users_roles(self):
        return UsersRoles


class AdmRoles(db.Model):
    def create_adm_roles(self):
        return Role


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('admin/index.html')
