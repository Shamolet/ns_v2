from flask import render_template
from app import db
from app.errors import errors


@errors.app_errorhandler(404)
def not_found_error(e):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500
