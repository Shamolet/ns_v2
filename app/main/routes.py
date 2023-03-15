from datetime import datetime
from flask import render_template, current_app
from flask_login import current_user, login_required
from app import db
from app.models.models import WOD
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# Index page 1 current WOD
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    wods = WOD.query.order_by(WOD.timestamp.desc()).paginate(
        per_page=current_app.config['WODS_PER_PAGE'], error_out=False)

    return render_template('index.html', title='Домашняя', wods=wods.items)
