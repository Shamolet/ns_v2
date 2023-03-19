from flask import Blueprint

adm = Blueprint('adm', __name__,  template_folder='templates', static_folder='static')

from app.admin import routes