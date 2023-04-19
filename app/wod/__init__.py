from flask import Blueprint

wod_bp = Blueprint('wod_bp', __name__)

# flake8: noqa
from app.wod import routes