import sqlite3
from database.db import get_connection
from utils.permissions import can_view_post


def get_posts(user=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()

    posts = [dict(p) for p in posts]

    visible_posts = [p for p in posts if can_view_post(user, p)]

    return visible_posts


def get_post(post_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()

    return dict(post) if post else None


def add_post(user_id, title, content, is_public):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (author_id, title, content, is_public) VALUES (?, ?, ?, ?)",
        (user_id, title, content, is_public),
    )
    conn.commit()
    conn.close()


def update_post(post_id, title, content, is_public):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE posts SET title = ?, content = ?, is_public = ? WHERE id = ?",
        (title, content, is_public, post_id),
    )
    conn.commit()
    conn.close()


def delete_post(post_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()


def get_username(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return user["username"] if user else None


def get_comments_for_post(user, post_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.*, u.username
        FROM comments c
        JOIN users u ON u.id = c.author_id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
        """,
        (post_id,),
    )

    comments = cursor.fetchall()
    conn.close()

    comments = [dict(c) for c in comments]

    if user is None or user["role"] == "user":
        comments = [c for c in comments if not c["is_hidden"]]

    return comments

def get_posts_with_authors(user=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT p.*, u.username AS author_username
        FROM posts p
        JOIN users u ON u.id = p.author_id
        ORDER BY p.created_at DESC
        """
    )
    posts = cursor.fetchall()
    conn.close()

    posts = [dict(p) for p in posts]

    visible_posts = [p for p in posts if can_view_post(user, p)]

    return visible_posts