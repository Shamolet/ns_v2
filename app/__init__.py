import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView
import os.path as op

from sqlalchemy import MetaData

# Instantiate Flask extensions
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy()
csrf_protect = CSRFProtect()
mail = Mail()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Пожалуйста, авторизируйтесь на сайте.'


def create_app(extra_config_settings={}):
    # Create a Flask applicaction.

    # Instantiate Flask
    app = Flask(__name__)
    # Load App Config settings
    # Load local settings from 'app/local_settings.py'
    app.config.from_object('app.local_settings')
    # Load extra config settings from 'extra_config_settings' param
    app.config.update(extra_config_settings)
    # Setup Flask-SQLAlchemy
    db.init_app(app)
    # Setup Flask-Mail
    mail.init_app(app)
    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)
    # Setup Bootstrap
    bootstrap.init_app(app)
    # Setup Moment
    moment.init_app(app)

    # Register blueprints
    # Errors
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    # Authentication
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # Main
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    # Admin
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Admin part
    class AdminUserView(ModelView):
        can_create = False
        column_display_pk = True
        column_exclude_list = ('password')
        form_overrides = dict(password=HiddenField)

    class AdmUsersRolesView(ModelView):
        column_display_pk = True

    class AdmRolesView(ModelView):
        column_display_pk = True

    # Admin model views
    from .models.admin_models import AdmUsers, AdmUsersRoles, AdmRoles
    admin = Admin(app, name='Нескучка', template_mode='bootstrap3', endpoint='admin')
    admin.add_view(AdminUserView(AdmUsers, db.session, name='Пользователь'))
    admin.add_view(AdmRolesView(AdmUsersRoles, db.session,
                                name='Roles-User'))
    admin.add_view(AdmUsersRolesView(AdmRoles, db.session, name='Роль'))
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Files'))

    # Main model views
    from .models.models import Comment, Exercise, WOD, Result
    admin.add_view(ModelView(Comment, db.session, name='Комментарии'))
    admin.add_view(ModelView(Exercise, db.session, name='Упражнения'))
    admin.add_view(ModelView(WOD, db.session, name='Упражнения'))
    admin.add_view(ModelView(Result, db.session, name='Результаты'))

    admin.add_link(MenuLink(name='Profile', endpoint='user.profile'))
    admin.add_link(MenuLink(name='Logout', endpoint='user.logout'))

    # Test and Debug
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='NS Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/ns.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('NS startup')

    return app
