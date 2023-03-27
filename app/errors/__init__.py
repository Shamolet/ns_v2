from flask import Blueprint

errors = Blueprint('errors', __name__)

# flake8: noqa
from app.errors import handlers
