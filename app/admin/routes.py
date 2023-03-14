from app.admin import bp
from flask import render_template


@bp.get('/admin')
def admin():
    return render_template('master-extended.html')