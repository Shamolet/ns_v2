from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)

# flake8: noqa
from app.auth import routes