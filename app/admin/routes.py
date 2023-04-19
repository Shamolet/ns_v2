from flask import render_template, redirect, url_for, flash, request
from flask_admin import expose, BaseView
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from werkzeug.urls import url_parse
from app import db
from app.admin import admin_bp
from app.forms.auth_forms import AdminLoginForm
from app.models.models import User


@admin_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


class MyAdmin(BaseView):
    @expose('/')
    def admin(self):
        return render_template('admin/admin.html', title='Админка')

    @expose('/login', methods=['GET', 'POST'])
    def admin_login(self):
        if current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('admin_bp.admin'))
        form = AdminLoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data)\
                    or not user.is_admin():
                flash("Нет доступа", "error")
                return redirect(url_for('admin_bp.admin_login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin_bp.admin')
            return redirect(next_page)
        return render_template('admin/admin_login.html', title='Войти', form=form)

    @expose('/logout')
    def admin_logout(self):
        logout_user()
        return redirect(url_for('auth_bp.login'))
