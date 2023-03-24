from flask import Blueprint

exercise = Blueprint('exercise', __name__)

from app.exercise import routes