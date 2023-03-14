from datetime import datetime
from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from app import db

# Define the User data model. Make sure to add the flask_user.UserMixin !!


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.Integer)  # (0) man (1) woman
    bith = db.Column(db.DateTime, nullable=False, default=None)
    about_me = db.Column(db.String(140))
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    registry = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    results = db.relationship('Result', backref='author', lazy='dynamic')
    wods = db.relationship('WOD', backref='author', lazy='dynamic')
    exercises = db.relationship('Exercise', backref='author', lazy='dynamic')
    roles = db.relationship('Role', secondary='users_roles', backref=db.backref('users', lazy='dynamic'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default=u'', unique=True)  # for @roles_accepted()
    # for display purposes
    label = db.Column(db.Unicode(255), server_default=u'')


# Define the UserRoles association model


class UsersRoles(db.Model):
    __tablename__ = 'users_roles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    pass

# Define the User profile form


class UserProfileForm(FlaskForm):
    pass
