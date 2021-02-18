from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap

bcrypt = Bcrypt()
mail = Mail()


def init_ext(app):
    bcrypt.init_app(app)
    mail.init_app(app)
    Bootstrap(app)


