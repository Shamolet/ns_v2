from flask import Blueprint

bp = Blueprint('User', __name__)

from app.user import routes
