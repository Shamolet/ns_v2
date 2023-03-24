from datetime import datetime
from flask import render_template
from flask_login import current_user, login_required
from app import db
from app.main import main


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Домашняя')

