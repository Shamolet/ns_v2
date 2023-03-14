from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Define the User data model.

class AdmUsers(db.Model):
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


class AdmUsersRoles(db.Model):
    __tablename__ = 'users_roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default=u'', unique=True)  # for @roles_accepted()
    # for display purposes
    label = db.Column(db.Unicode(255), server_default=u'')


class AdmRoles(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    # for display purposes
    label = db.Column(db.Unicode(255), server_default=u'')
