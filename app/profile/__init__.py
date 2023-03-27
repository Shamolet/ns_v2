from flask import Blueprint

profile = Blueprint('profile', __name__)

# flake8: noqa
from app.profile import routes
