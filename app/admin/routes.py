from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user, login_user
from flask_security import SQLAlchemyUserDatastore, Security
from werkzeug.urls import url_parse

from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_admin import expose, BaseView, Admin, AdminIndexView

from app.forms.auth_forms import LoginForm
from app.models.models import User, Role
from ns import app


# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)

class MyAdmin(AdminIndexView):
    @expose('/')
    def admin(self):
        return render_template('admin/admin.html')


# @admin_bp.before_app_request
# def is_accessible():
#     return (current_user.is_active and
#             current_user.is_authenticated )
#
# class AdminView(BaseView):
#     @expose('/', methods=('GET', 'POST'))
#     def admin(self):
#         if current_user.is_authenticated:
#             return redirect(url_for('.admin'))
#         form = LoginForm()
#         if form.validate_on_submit():
#             user = User.query.filter_by(username=form.username.data).first()
#             if user is None or not user.check_password(form.password.data):
#                 flash("Неверная пара логин/пароль", "error")
#                 return redirect(url_for('auth.login'))
#             login_user(user, remember=form.remember_me.data)
#             next_page = request.args.get('next')
#             if not next_page or url_parse(next_page).netloc != '':
#                 next_page = url_for('main.index')
#             return redirect(next_page)
#         return render_template('auth/login.html', title='Войти', form=form)

# Indivirual Admin part
class AdminUserView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['username']


class AdmExerciseView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['exercise_name', 'ip', 'description', 'note']


class AdmWODView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['wod_name', 'warm_up', 'workout', 'description']


class AdmCommentView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['body']


class AdmResultView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    form_columns = ['result']

    # # Admin model views


admin = Admin(app, name='Админка', template_mode='bootstrap3')

# # Main model views
from app.models.models import User, Comment, Exercise, WOD, Result

admin.add_view(AdminUserView(User, db.session, name='Пользователь'))
admin.add_view(AdmWODView(WOD, db.session, name='Тренировки'))
admin.add_view(AdmExerciseView(Exercise, db.session, name='Упражнения'))
admin.add_view(AdmCommentView(Comment, db.session, name='Комментарии'))
admin.add_view(AdmResultView(Result, db.session, name='Результаты'))

admin.add_link(MenuLink(name='Выход', endpoint='admin.index'))
