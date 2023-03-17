from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.user.auth import routes