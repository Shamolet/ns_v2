from datetime import timedelta
import os

from dotenv import load_dotenv

# Takes the location of the database
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# *****************************
# Environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#    python -c "import os; print(repr(os.urandom(24)));"
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
COOKIE_SECURE = 'Secure'
COOKIE_DURATION = timedelta(days=365)

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids a SQLAlchemy Warning


# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps"
# to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps
# (near the bottom).


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'yourname@gmail.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"Your Name" <yourname@gmail.com>'

ADMINS = [
    '"Admin One" <admin1@gmail.com>',
]
