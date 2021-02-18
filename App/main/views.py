from flask import render_template, request, Blueprint
from App.models import Post

main = Blueprint('main', __name__)


def init_main(app):
    app.register_blueprint(blueprint=main)


@main.route('/')
@main.route('/home/')
def home():
    # page is given using query string
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.time.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts)


@main.route('/about/')
def about():
    return render_template('about.html', title='About')















