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


@main.route('/wod')
def wod():
    return render_template('main/wods.html', title='Тренировки')


@main.route('/exercises')
def exercises():
    return render_template('main/exercises_list.html', title='Каталог движений')


@main.route('/exercises/<modality>')
def mode(modality):

    return render_template('main/modality_list.html', modality=modality, title='Модальность')


@main.route('/exercises/<modality>/<exercise_name>')
def exercise(modality, exercise_name):

    return render_template('main/exercise_name.html', exercise_name=exercise_name,
                           modality=modality, title=exercise)


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return render_template('main/admin.html')
