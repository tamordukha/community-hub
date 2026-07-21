from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort
from models.like import toggle_like_post, toggle_like_comment, toggle_like_reply


likes_bp = Blueprint('likes', __name__)


@likes_bp.route("/<int:post_id>/like", methods=["POST"])
def like_post_index(post_id):
    if not session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    toggle_like_post(post_id, user_id)
    return redirect(url_for("posts.index"))

@likes_bp.route("/post/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    if not session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    toggle_like_post(post_id, user_id)
    return redirect(url_for("posts.show_post", post_id=post_id))


@likes_bp.route("/post/<int:post_id>/<int:comment_id>/like", methods=["POST"])
def like_comment(post_id, comment_id):
    if not session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    toggle_like_comment(comment_id, user_id)
    return redirect(url_for("posts.show_post", post_id=post_id))


@likes_bp.route("/post/<int:post_id>/<int:reply_id>/like", methods=["POST"])
def like_reply(post_id, reply_id):
    if not session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    toggle_like_reply(reply_id, user_id)
    return redirect(url_for("posts.show_post", post_id=post_id))
