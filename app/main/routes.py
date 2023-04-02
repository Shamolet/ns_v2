from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_admin import BaseView, expose
from flask_login import current_user, login_required
from app import db
from app.forms.forms import EditProfileForm
from app.main import main
from app.models.models import User, Exercise


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username': 'KIM'}
    return render_template('index.html', title='Домашняя', user=user)


# Block Users
@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('main/profile.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('main/edit_profile.html', title='Редактировать профиль',
                           form=form)


# Block WODs lib
@main.route('/wods')
def wods_list():
    return render_template('main/wods_list.html', title='Список тренировок')


@main.route('/wods/<wod>')
def wod_name(wod):
    return render_template('main/wod.html', wod=wod, title='Тренировка дня')


# Block Exercises Lib
@main.route('/exercises')
def exercises():
    exercises_list = Exercise.query.order_by(Exercise.exercise_name.asc()).all()
    return render_template('main/exercises_list.html',
                           exercises_list=exercises_list, title='Каталог движений')


@main.route('/exercises/<int:id>')
def exercise_detail(id):
    detail = Exercise.query.get(id)
    return render_template('main/exercise_detail.html',
                           detail=detail)


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return render_template('main/admin.html')
