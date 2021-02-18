import secrets, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'App/static')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'App/templates')


class SQLiteConfig:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite3.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = ''
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ('Display Name', 'noreply@demo.com')


def get_db_uri(DATABASE):
    ENGINE = DATABASE.get('ENGINE')
    DRIVER = DATABASE.get('DRIVER')
    USER = DATABASE.get('USER')
    PASSWORD = DATABASE.get('PASSWORD')
    HOST = DATABASE.get('HOST')
    PORT = DATABASE.get('PORT')
    NAME = DATABASE.get('NAME')
    return "{}+{}://{}:{}@{}:{}/{}".format(ENGINE, DRIVER, USER, PASSWORD, HOST, PORT, NAME)


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'GEPEI LU'
    SESSION_TYPE = 'redis'
    # session['user'] = user_id


class DevelopConfig(Config):
    DEBUG = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '14121314',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flask'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class TestingConfig(Config):
    TESTING = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '14121314',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flask'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


envs = {
    'develop': DevelopConfig,
    'testing': TestingConfig
}