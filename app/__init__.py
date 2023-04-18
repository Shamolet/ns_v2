import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_admin.menu import MenuLink
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import MetaData
from config import Config

# Instantiate Flask extensions
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
csrf_protect = CSRFProtect()
mail = Mail()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Пожалуйста, авторизируйтесь на сайте.'


def create_app(config_class=Config):
    # Create a Flask applicaction.
    # Instantiate Flask
    app = Flask(__name__)
    # Load App Config settings
    app.config.from_object(config_class)
    # Setup Flask-SQLAlchemy
    db.init_app(app)
    # Setup Flask-Migrate
    migrate.init_app(app, db)
    # Setup Flask-Mail
    mail.init_app(app)
    # Setup Flask-Login
    login.init_app(app)
    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)
    # Setup Bootstrap
    bootstrap.init_app(app)
    # Setup Moment
    moment.init_app(app)

    # Register blueprints
    # Main
    from app.main import main
    app.register_blueprint(main)
    # Authentication
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    # Admin
    from app.admin import admin_bp
    app.register_blueprint(admin_bp)
    # Errors
    from app.errors import errors
    app.register_blueprint(errors)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    class AdminUserView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        can_view_details = True
        column_exclude_list = ['password_hash']
        form_excluded_columns = ['password_hash']

        form_columns = ['username', 'sex', 'admin']

    class AdminExerciseView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        can_view_details = True

        form_columns = ['exercise_name', 'ip', 'description', 'note', 'modality']

    class AdminWODView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        can_view_details = True

        form_columns = ['wod_name', 'warm_up', 'workout', 'description', 'confirm']

    class AdminCommentView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        can_view_details = True

        form_columns = ['body']

    class AdminResultView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        can_view_details = True

        form_columns = ['result']

    # # Admin model views
    admin = Admin(app, name='Админка', template_mode='bootstrap3')
    #
    # # Main model views
    from app.models.models import User, Comment, Exercise, WOD, Result_rep
    admin.add_view(AdminUserView(User, db.session, name='Пользователь'))
    admin.add_view(AdminWODView(WOD, db.session, name='Тренировки'))
    admin.add_view(AdminExerciseView(Exercise, db.session, name='Упражнения'))
    admin.add_view(AdminCommentView(Comment, db.session, name='Комментарии'))
    admin.add_view(AdminResultView(Result_rep, db.session, name='Результаты'))

    admin.add_link(MenuLink(name='Выход', endpoint='main.index'))

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

        # logs
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
