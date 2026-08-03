from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort, jsonify
from models.like import toggle_like_post, toggle_like_comment, toggle_like_reply
from database.db import get_connection


likes_bp = Blueprint('likes', __name__)


@likes_bp.route("/post/like", methods=["POST"])
def like_post():
    if not session:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    redirect_to = request.form.get("redirect_to", "index")
    post_id = request.form.get("post_id")
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400
    toggle_like_post(post_id, user_id)

    # Считаем новое количество лайков
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM post_likes WHERE post_id = ?", (post_id,))
    count = cursor.fetchone()[0]

    # Проверяем, лайкнул ли сейчас пользователь
    cursor.execute(
        "SELECT id FROM post_likes WHERE user_id = ? AND post_id = ?",
        (user_id, post_id),
    )
    liked = cursor.fetchone() is not None
    conn.close()

    # Если AJAX — возвращаем JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"liked": liked, "count": count})
    
    # Иначе — обычный редирект
    if redirect_to == "post":
        return redirect(url_for("posts.show_post", post_id=post_id))
    return redirect(url_for("posts.index"))






@likes_bp.route("/comment/like", methods=["POST"])
def like_comment():
    if not session:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    post_id = request.form.get("post_id")
    comment_id = request.form.get("comment_id")
    if not post_id:
            return jsonify({"error": "Missing post_id"}), 400
    if not comment_id:
        return jsonify({"error": "Missing comment_id"}), 400
    
    toggle_like_comment(comment_id, user_id)

    # Считаем новое количество лайков
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM comment_likes WHERE comment_id = ?", (comment_id,))
    count = cursor.fetchone()[0]

    # Проверяем, лайкнул ли сейчас пользователь
    cursor.execute(
        "SELECT id FROM comment_likes WHERE user_id = ? AND comment_id = ?",
        (user_id, comment_id),
    )
    liked = cursor.fetchone() is not None
    conn.close()

    # Если AJAX — возвращаем JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"liked": liked, "count": count})
    
    # Иначе — обычный редирект
    return redirect(url_for("posts.show_post", post_id=post_id))


@likes_bp.route("/reply/like", methods=["POST"])
def like_reply():
    if not session:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    post_id = request.form.get("post_id")
    reply_id = request.form.get("reply_id")
    if not post_id:
            return jsonify({"error": "Missing post_id"}), 400
    if not reply_id:
        return jsonify({"error": "Missing reply_id"}), 400
    
    toggle_like_reply(reply_id, user_id)

    # Считаем новое количество лайков
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reply_likes WHERE reply_id = ?", (reply_id,))
    count = cursor.fetchone()[0]

    # Проверяем, лайкнул ли сейчас пользователь
    cursor.execute(
        "SELECT id FROM reply_likes WHERE user_id = ? AND reply_id = ?",
        (user_id, reply_id),
    )
    liked = cursor.fetchone() is not None
    conn.close()

    # Если AJAX — возвращаем JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"liked": liked, "count": count})
    
    # Иначе — обычный редирект
    return redirect(url_for("posts.show_post", post_id=post_id))
