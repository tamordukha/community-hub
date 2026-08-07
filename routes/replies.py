from flask import Blueprint, request, redirect, url_for, session, abort
from models.reply import get_reply, add_reply, add_reply_to_reply, update_reply, delete_reply, hide_reply
from models.post import get_post
from models.comment import get_comment
from utils.permissions import can_edit_reply, can_delete_reply, can_hide_reply

replies_bp = Blueprint('replies', __name__)

@replies_bp.route("/post/<int:post_id>/<int:comment_id>/reply/create", methods=["POST"])
def create_reply(post_id, comment_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    content = request.form.get("content")
    if not content or not content.strip():
        return redirect(url_for("posts.show_post", post_id=post_id))

    user_id = session["user_id"]
    content = content.strip()
    add_reply(user_id, comment_id, content)
    print(f"Creating reply: user={user_id}, comment={comment_id}, content={content}")
    return redirect(url_for("posts.show_post", post_id=post_id))

@replies_bp.route("/post/<int:post_id>/<int:comment_id>/reply/<int:parent_reply_id>/reply-to-reply", methods=["POST"])
def create_reply_to_reply(post_id, comment_id, parent_reply_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    content = request.form.get("content")
    if not content or not content.strip():
        return redirect(url_for("posts.show_post", post_id=post_id))

    user_id = session["user_id"]
    content = content.strip()
    add_reply_to_reply(user_id, comment_id, parent_reply_id, content)
    return redirect(url_for("posts.show_post", post_id=post_id))


@replies_bp.route("/post/<int:post_id>/reply/<int:reply_id>/edit", methods=["POST"])
def edit_reply(post_id, reply_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user = {"id": session["user_id"], "role": session["role"]}
    reply = get_reply(reply_id)

    if reply is None:
        abort(404)
    if not can_edit_reply(user, reply):
        abort(403)

    content = request.form.get("content")
    if content and content.strip():
        content = content.strip()
        update_reply(reply_id, content)

    return redirect(url_for("posts.show_post", post_id=post_id))


@replies_bp.route("/post/<int:post_id>/reply/<int:reply_id>/delete", methods=["POST"])
def del_reply(post_id, reply_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user = {"id": session["user_id"], "role": session["role"]}
    reply = get_reply(reply_id)

    if reply is None:
        abort(404)
    if not can_delete_reply(user, reply):
        abort(403)

    delete_reply(reply_id)
    return redirect(url_for("posts.show_post", post_id=post_id))


@replies_bp.route("/post/<int:post_id>/reply/<int:reply_id>/hide", methods=["POST"])
def toggle_hide_reply(post_id, reply_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user = {"id": session["user_id"], "role": session["role"]}
    reply = get_reply(reply_id)

    if reply_id is None:
        abort(404)

    comment = get_comment(reply["comment_id"])
    post_id = comment["post_id"]
    post = get_post(post_id)
    if not can_hide_reply(user, post, reply):
        abort(403)

    hide_reply(reply_id)
    return redirect(url_for("posts.show_post", post_id=post_id))