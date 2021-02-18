from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from App.ext import bcrypt
from App.models import db, User, Post
from App.users.forms import RegisterForm, LoginForm, UpdateProfileForm, RequestResetPasswordForm, ResetPasswordForm
from App.users.utils import save_image, delete_image, send_reset_email

users = Blueprint('users', __name__)


def init_users(app):
    app.register_blueprint(blueprint=users)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()

        flash('Account Created for {}!'.format(username), category='success')
        return redirect(url_for('users.login'))
    else:
        return render_template('register.html', title='Register', form=form, legend='Join Now')


@users.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login failed, please check email or password!', category='danger')
    return render_template('login.html', title='Login', form=form, legend='Login')


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            new_filename = save_image(form.image.data)
            old_filename = current_user.image_file
            delete_image(old_filename)
            current_user.image_file = new_filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You profile has been update', category='success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)


@users.route('/user/<string:username>/')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.time.desc()).paginate(per_page=5, page=page)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password/', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', category='info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password')


@users.route('/reset_password/<string:token>/', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('Token is invalid or expired', category='warning')
        return redirect(url_for('users.reset_request'))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            password = form.password.data
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()

            flash('Reset password succeed!', category='success')
            return redirect(url_for('users.login'))
        return render_template('reset_token.html', title='Reset Password', form=form, legend='Reset Password')