from flask import Blueprint

exercise = Blueprint('exercise', __name__)

# flake8: noqa
from app.exercise import routes