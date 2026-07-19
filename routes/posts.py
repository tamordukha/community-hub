from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort
from models.post import get_posts, get_post, add_post, update_post, delete_post, get_username, get_username, get_posts_with_authors, get_post_with_author
from models.comment import get_comments_for_post
from models.reply import get_replies_for_post, get_replies_count

from utils.permissions import can_edit_post, can_delete_post, can_edit_comment, can_delete_comment, can_hide_comment, can_edit_reply, can_delete_reply, can_hide_reply

posts_bp = Blueprint('posts', __name__)

@posts_bp.route("/")
def index():
    if not session:
        user = None
        current_username = None
    else:
        user = {
            "id": session.get("user_id"),
            "role": session.get("role")
        }
        current_username = get_username(user["id"])
    posts = get_posts_with_authors(user)

    return render_template("posts/index.html", posts=posts, current_username=current_username, show_bottom_bar=True)


@posts_bp.route("/post/<int:post_id>")
def show_post(post_id):
    if not session:
        user = None
    else:
        user = {
            "id": session.get("user_id"),
            "role": session.get("role")
        }
    post = get_post_with_author(post_id)
    if post is None:
        abort(404)
    comments = get_comments_for_post(user, post_id)
    replies = get_replies_for_post(user, post_id)
    replies_count = get_replies_count(user, post_id)

    return render_template(
        "posts/view.html", 
        post=post, comments=comments, replies=replies, replies_count=replies_count ,user=user,
        can_edit_post=can_edit_post,
        can_delete_post=can_delete_post, 
        can_edit_comment=can_edit_comment, can_edit_reply=can_edit_reply,
        can_delete_comment=can_delete_comment, can_delete_reply=can_delete_reply,
        can_hide_comment=can_hide_comment, can_hide_reply=can_hide_reply
        )


@posts_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        is_public = int(request.form.get('is_public', 1))
        if not title or not content:
            return render_template("posts/index.html", error="Title and content are required")
        add_post(user_id, title, content, is_public)
        return redirect(url_for("posts.index"))
    
    return render_template("posts/create.html")


@posts_bp.route("/post/edit/<int:post_id>", methods=["GET","POST"])
def edit_post(post_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    user = {"id": session["user_id"], "role": session["role"]}
    post = get_post(post_id)
    if post is None:
        abort(404)
    if not can_edit_post(user, post):
        abort(403)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        is_public = int(request.form.get('is_public', 1))
        post_id = post["id"]
        if not title or not content:
            return render_template("posts/edit.html", post=post, error="Title and content are required")
        update_post(post_id, title, content, is_public)
        return redirect(url_for("posts.show_post", post_id=post_id))
    
    return render_template("posts/edit.html", post=post)

@posts_bp.route("/post/delete/<int:post_id>", methods=["POST"])
def del_post(post_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    user = {"id": session["user_id"], "role": session["role"]}
    post = get_post(post_id)
    if post is None:
        abort(404)
    if not can_delete_post(user, post):
        abort(403)
    delete_post(post_id)
    return redirect(url_for("posts.index"))