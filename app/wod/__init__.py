from flask import Blueprint

wod = Blueprint('wod', __name__)

from app.wod import routes