from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.forms.forms import EditProfileForm, EmptyForm, CommentForm
from app.models.models import User, Comment
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# WOD page
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Твой коммент опубликован!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    comments = current_user.followed_posts().paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.index', page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.index', page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('index.html', title='Домашняя', form=form,
                           posts=comments.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.explore', page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.explore', page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('index.html', title='Поиск',
                           posts=comments.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = user.comments.order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.user', username=user.username,
                       page=comments.next_num) if comments.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=comments.prev_num) if comments.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, comments=comments.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
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
    return render_template('edit_profile.html', title='Редактировать профиль',
                           form=form)
