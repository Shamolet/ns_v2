from flask import Blueprint

auth = Blueprint('auth', __name__)

# flake8: noqa
from app.auth import routes