from werkzeug.urls import url_parse
from app.admin import adm
from flask import render_template, redirect, url_for, flash, request
from app.constants import USER
from app.forms.auth_forms import LoginForm
from flask_login import login_user, logout_user, login_required
from app.models.models import User


@adm.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,
                                    role=USER.ADMIN).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный пароль и/или имя пользователя')
            return redirect(url_for('admin.entry'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('admin.admin.html', title='Админ-панель', form=form)


@adm.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
