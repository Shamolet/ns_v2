from datetime import datetime
from werkzeug.urls import url_parse

from app import db
from app.admin import adm
from flask import render_template, redirect, url_for, flash, request
from app.constants import USER
from app.forms.auth_forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import User


@adm.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@adm.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,
                                    role=USER.ADMIN).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный пароль и/или имя пользователя')
            return redirect(url_for('admin.admin_login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.admin_login')
        return redirect(next_page)
    return render_template('admin.admin.html', title='Админ-панель', form=form)


@adm.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))
