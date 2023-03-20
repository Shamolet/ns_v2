import sqlite3
from datetime import datetime
from flask import render_template
from flask_login import current_user
from app import db
from app.models.models import WOD
from app.main import main


# @main.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()



@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def listwod():
    for i in range(3):
        if not len(WOD.query.all()) >= 3:
            wod = WOD(date_posted=wod.date_posted(), wod_name=wod.wod_name(), description=wod.description())
            db.session.add(wod)
            db.session.commit()

    all_wods = WOD.query.all()

    return render_template('index.html', title='Домашняя', all_wods=all_wods)
