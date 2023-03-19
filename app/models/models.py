from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import jwt
from time import time

from app.constants import OTHER, ACTIVE, USER


# Define the User data model.
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # User authentication information
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.Unicode(255), nullable=False,
                      server_default=u'', unique=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.SmallInteger, default=OTHER)  # look at constants.py
    bith = db.Column(db.DateTime, nullable=False, default=None)
    about_me = db.Column(db.String(280))
    status = db.Column(db.SmallInteger, default=ACTIVE)  # look at constants.py
    # User information
    registry = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.SmallInteger, default=USER)  # look at constants.py
    # Relationships
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    results = db.relationship('Result', backref='author', lazy='dynamic')
    wods = db.relationship('WOD', backref='author', lazy='dynamic')
    exercises = db.relationship('Exercise', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

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
        except:
            return
        return User.query.get(id)

# Flask-Login profile loader function
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Define the Comment data model.
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)


# Define the Exercise data model.
class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(280), unique=True, nullable=False)
    description = db.Column(db.Text(200), nullable=False)
    modality = db.Column(db.Integer, unique=False, nullable=False)
    # modality (0) metabolic (1) gymnastic (2) external object
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    wod_id = db.Column(db.Integer, db.ForeignKey("wods.id"))


# Define the WOD data model.
class WOD(db.Model):
    __tablename__ = "wods"

    id = db.Column(db.Integer, primary_key=True)
    wod_name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.Text(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    exercises = db.relationship("exercises.id", backref='author', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)


# Define the Results data model.
class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    # think about post results: load, time, reps
    result = db.Column(db.String(200), unique=False, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # Relationship User, Exercise
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    exercises = db.relationship("exercises.id", backref='author', lazy=True)
