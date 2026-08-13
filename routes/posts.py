from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort, jsonify
from models.post import get_posts, get_post, add_post, update_post, delete_post
from models.user import get_user_by_id
from models.comment import get_comments_for_post
from models.reply import get_replies_for_post, get_replies_count

from utils.permissions import can_edit_post, can_delete_post, can_edit_comment, can_delete_comment, can_hide_comment, can_edit_reply, can_delete_reply, can_hide_reply
from config import Config

posts_bp = Blueprint('posts', __name__)

@posts_bp.route("/")
def index():
    if not session.get("user_id"):
        user = None
        current_username = None
    else:
        user = {
            "id": session.get("user_id"),
            "role": session.get("role")
        }
        current_username = get_user_by_id(user["id"])["username"]
    posts = get_posts(user)
    print(session)

    return render_template("posts/index.html", posts=posts, current_username=current_username, show_bottom_bar=True)


@posts_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    if not session.get("user_id"):
        user = None
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "Unauthorized"}), 401
    else:
        user = {
            "id": session.get("user_id"),
            "role": session.get("role")
        }
    post = get_post(post_id, user)
    if post is None:
        abort(404)
    sort = request.form.get("sort-input", "1")
    print("SORT IN ROUTE:", sort)
    comments = get_comments_for_post(post_id, user, sort)
    replies = get_replies_for_post(post_id, user)
    replies_count = get_replies_count(user, post_id)

    return render_template(
        "posts/view.html", 
        post=post, comments=comments, replies=replies, replies_count=replies_count ,user=user, sort=sort,
        can_edit_post=can_edit_post,
        can_delete_post=can_delete_post, 
        can_edit_comment=can_edit_comment, can_edit_reply=can_edit_reply,
        can_delete_comment=can_delete_comment, can_delete_reply=can_delete_reply,
        can_hide_comment=can_hide_comment, can_hide_reply=can_hide_reply
        )


@posts_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        is_public = int(request.form.get('is_public', 1))
        if not title or not content:
            return render_template("posts/index.html", error="Title and content are required")
        if len(content) > Config.POST_MAX_LENGTH:
            return render_template("posts/create.html", error=f"Max {Config.POST_MAX_LENGTH} characters")
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
        if len(content) > Config.POST_MAX_LENGTH:
            return render_template("posts/edit.html", error=f"Max {Config.POST_MAX_LENGTH} characters")
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