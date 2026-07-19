from flask import Blueprint, request, redirect, url_for, session, abort
from models.comment import get_comment, add_comment, update_comment, delete_comment, hide_comment
from models.post import get_post
from utils.permissions import can_edit_comment, can_delete_comment, can_hide_comment

comments_bp = Blueprint('comments', __name__)


@comments_bp.route("/post/<int:post_id>/comment/create", methods=["POST"])
def create_comment(post_id):
    if not session:
        return redirect(url_for("auth.login"))

    content = request.form.get("content")
    if not content or not content.strip():
        return redirect(url_for("posts.show_post", post_id=post_id))

    user_id = session["user_id"]
    content = content.strip()
    add_comment(user_id, post_id, content)
    return redirect(url_for("posts.show_post", post_id=post_id))


@comments_bp.route("/post/<int:post_id>/comment/<int:comment_id>/edit", methods=["POST"])
def edit_comment(post_id, comment_id):
    if not session:
        return redirect(url_for("auth.login"))

    user = {"id": session["user_id"], "role": session["role"]}
    comment = get_comment(comment_id)

    if comment is None:
        abort(404)
    if not can_edit_comment(user, comment):
        abort(403)

    content = request.form.get("content")
    if content and content.strip():
        content = content.strip()
        update_comment(comment_id, content)

    return redirect(url_for("posts.show_post", post_id=post_id))


@comments_bp.route("/post/<int:post_id>/comment/<int:comment_id>/delete", methods=["POST"])
def del_comment(post_id, comment_id):
    if not session:
        return redirect(url_for("auth.login"))

    user = {"id": session["user_id"], "role": session["role"]}
    comment = get_comment(comment_id)

    if comment is None:
        abort(404)
    if not can_delete_comment(user, comment):
        abort(403)

    delete_comment(comment_id)
    return redirect(url_for("posts.show_post", post_id=post_id))


@comments_bp.route("/post/<int:post_id>/comment/<int:comment_id>/hide", methods=["POST"])
def toggle_hide_comment(post_id, comment_id):
    if not session:
        return redirect(url_for("auth.login"))

    user = {"id": session["user_id"], "role": session["role"]}
    comment = get_comment(comment_id)

    if comment is None:
        abort(404)
    post_id = comment["post_id"]
    post = get_post(post_id)
    if not can_hide_comment(user, post, comment):
        abort(403)

    hide_comment(comment_id)
    return redirect(url_for("posts.show_post", post_id=post_id))