from flask import Blueprint

admin_bp = Blueprint('admin_blueprint', __name__)

# flake8: noqa
from app.admin import routes