from flask import Blueprint

wod = Blueprint('wod', __name__)

# flake8: noqa
from app.wod import routes
