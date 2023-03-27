from flask import Blueprint

adm = Blueprint('adm', __name__)

# flake8: noqa
from app.admin import routes
