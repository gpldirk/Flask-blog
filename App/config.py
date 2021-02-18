import secrets, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'App/static')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'App/templates')


class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite3.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = '{{your email name}}'
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_PASSWORD = '{{your email password}}'
    MAIL_DEFAULT_SENDER = ('Display Name', 'noreply@demo.com')