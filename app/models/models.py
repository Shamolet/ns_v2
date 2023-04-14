from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import jwt
from time import time

from app import constants


# Define the User data model.
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # User authentication information
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.SmallInteger, default=constants.OTHER)  # look at constants.py
    birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    about_me = db.Column(db.String(280))
    status = db.Column(db.SmallInteger, default=constants.ACTIVE)  # look at constants.py
    # User information
    registry = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Admin
    admin = db.Column(db.Boolean())

    # Relationships
    user_comments = db.relationship('Comment', backref='author_comment', lazy='dynamic')


    def is_admin(self):
        return self.admin

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Required for administrative interface
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)


# Flask-Login profile loader function @login_required
@login.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


# Define the Comment data model.
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    wod_id = db.Column(db.Integer, db.ForeignKey('wods.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)


# Define the WOD data model.
class WOD(db.Model):
    __tablename__ = "wods"

    id = db.Column(db.Integer, primary_key=True)
    wod_name = db.Column(db.String(100), unique=False, nullable=False, default=None)
    warm_up = db.Column(db.Text(200), nullable=False)
    workout = db.Column(db.Text(200), nullable=False)
    description = db.Column(db.Text(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # Relationship User(Many), Comment() Exercise
    wod_comments = db.relationship("Comment", backref='wod_comment', lazy=True)


# Define the Exercise data model.
class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(280), unique=True, nullable=False)
    ip = db.Column(db.Text(200), nullable=False)
    description = db.Column(db.Text(200), nullable=False)
    note = db.Column(db.Text(200), nullable=False)
    modality = db.Column(db.SmallInteger, default=constants.METABOLIC)
    # modality (0) metabolic (1) gymnastic (2) external object
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # wod_id = db.Column(db.Integer, db.ForeignKey("wods.id"), nullable=False)




# Define the Results data model.
class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    # think about post results: load, time, reps
    result = db.Column(db.String(200), unique=False, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # Relationship User, Exercise
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # exercises = db.relationship("exercises.id", backref='author', lazy=True)
