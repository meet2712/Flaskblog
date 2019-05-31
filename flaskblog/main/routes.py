from flask import render_template, request, Blueprint, redirect, url_for, flash
from flaskblog.models import User, Post, Comment
from flaskblog import db


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/admin/")
def admin():
    return render_template('admin.html', title='admin', user=User.query.all(), post=Post.query.all())


@main.route("/admin/<int:post_id1>/delete")
def delete_post1(post_id1):
    post = Post.query.get_or_404(post_id1)
    post1 = Comment.query.get_or_404(post_id1)
    db.session.delete(post1)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.admin'))


@main.route("/admin/<int:user_id>/delete_user")
def delete_user(user_id):
    post1 = Post.query.get_or_404(user_id)
    post = User.query.get_or_404(user_id)
    db.session.delete(post1)
    db.session.delete(post)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('main.admin'))
