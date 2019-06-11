from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post,Comment
from flaskblog.posts.forms import PostForm, AddCommentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = AddCommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(body=form.body.data, post_id=post.id, path=0)
            db.session.add(comment)
            db.session.commit()
            str2 = "select id from Comment order by id desc limit 1"
            result2 = (db.session.execute(str2).fetchall())
            for r in result2:
                pid = r[0]
           # print(pid)
            str3 = "update comment set path = {} where id = {}".format(pid, pid)
            db.session.execute(str3)
            db.session.commit()
            flash("Your comment has been added to the post", "success")
            return redirect(url_for("main.home"))
    return render_template("comment_post.html", title="Comment Post", form=form, post_id=post_id)


@posts.route("/post/<int:post_id>/comment/<comment_id>/reply", methods=["GET", "POST"])
@login_required
def reply_comment(post_id,comment_id):
    post = Post.query.get_or_404(post_id)
   # comment = Comment.query.get(comment_id)
    parent = Comment.query.get(comment_id)
    path = str(comment_id)
    db.session.commit()
    form = AddCommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(body=form.body.data, post_id=post.id, parent_id=comment_id, depth=parent.depth+1, path=path)
            db.session.add(comment)
            db.session.commit()
            child = Comment.query.get(comment.id)
           # print(child)
            child.path = str(parent.path)+'.'+str(child.id)
            db.session.commit()
            flash("Your reply has been added to the post", "success")
            return redirect(url_for("main.home"))
    return render_template("reply_comment.html", title="Comment Post", form=form, post_id=post_id, comment_id=comment_id)