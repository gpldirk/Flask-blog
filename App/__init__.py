from flask import Flask
from App.config import Config, STATIC_FOLDER, TEMPLATES_FOLDER
from App.errors.views import init_errors
from App.ext import init_ext
from App.main.views import init_main
from App.models import init_db
from App.posts.views import init_posts
from App.users.views import init_users


def create_app(config=Config):
    app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATES_FOLDER)
    app.config.from_object(Config)

    init_db(app)
    init_users(app)
    init_posts(app)
    init_main(app)
    init_errors(app)
    init_ext(app)
    return app

