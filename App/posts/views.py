
from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from App.models import db
from App.models import Post
from App.posts.forms import PostForm

posts = Blueprint('posts', __name__)


def init_posts(app):
    app.register_blueprint(blueprint=posts)


@posts.route('/post/new/', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created!', category='success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('update_post.html', title="Update Post", form=form, legend='Update Post')
    elif request.method == 'POST':
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your post has been updated!', category='success')
            return redirect(url_for('posts.post', post_id=post.id))


@posts.route('/post/<int:post_id>/delete', methods=['post'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('users.user_posts', username=current_user.username))


@posts.route('/post/<int:post_id>/')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
