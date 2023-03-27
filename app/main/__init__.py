from flask import Blueprint

main = Blueprint('main', __name__)

# flake8: noqa
from app.main import routes
