import sqlite3
from database.db import get_connection
from utils.permissions import can_view_post


def get_posts(user=None, profile_user_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        if user:
            query = """
                SELECT 
                    p.*, u.username AS author_username, u.avatar AS author_avatar,
                    (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id) AS like_count,
                    (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id AND user_id = ?) AS liked_by_current_user,
                    (
                        (SELECT COUNT(*) FROM comments WHERE post_id = p.id) + 
                        (SELECT COUNT(*) FROM replies WHERE comment_id IN (SELECT id FROM comments WHERE post_id = p.id))
                    ) AS comment_count
                FROM posts p
                JOIN users u ON u.id = p.author_id
                ORDER BY p.created_at DESC
            """
            cursor.execute(query, (user["id"],))
        else:
            query = """
                SELECT 
                    p.*, u.username AS author_username, u.avatar AS author_avatar,
                    (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id) AS like_count,
                    (
                        (SELECT COUNT(*) FROM comments WHERE post_id = p.id) + 
                        (SELECT COUNT(*) FROM replies WHERE comment_id IN (SELECT id FROM comments WHERE post_id = p.id))
                    ) AS comment_count
                FROM posts p
                JOIN users u ON u.id = p.author_id
                ORDER BY p.created_at DESC
            """
            cursor.execute(query)
        posts = cursor.fetchall()

    posts_dicts = [dict(p) for p in posts]

    if profile_user_id:
        visible_posts = [p for p in posts_dicts if can_view_post(user, p) and p["author_id"]==profile_user_id]
    else:
        visible_posts = [p for p in posts_dicts if can_view_post(user, p)]

    return visible_posts


def get_post(post_id, user=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        if user:
            query = """
                SELECT 
                    p.*, u.username AS author_username, u.avatar AS author_avatar,
                    (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id) AS like_count,
                    (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id AND user_id = :user_id) AS liked_by_current_user,
                    (
                        (SELECT COUNT(*) FROM comments WHERE post_id = p.id) + 
                        (SELECT COUNT(*) FROM replies WHERE comment_id IN (SELECT id FROM comments WHERE post_id = p.id))
                    ) AS comment_count
                FROM posts p
                JOIN users u ON u.id = p.author_id
                WHERE p.id = :post_id
            """
            cursor.execute(query, {"post_id": post_id, "user_id": user["id"]})
        else:
            query = """
                SELECT 
                    p.*, u.username AS author_username, u.avatar AS author_avatar,
                    (SELECT COUNT(*) FROM post_likes WHERE post_id = p.id) AS like_count,
                    (
                        (SELECT COUNT(*) FROM comments WHERE post_id = p.id) + 
                        (SELECT COUNT(*) FROM replies WHERE comment_id IN (SELECT id FROM comments WHERE post_id = p.id))
                    ) AS comment_count
                FROM posts p
                JOIN users u ON u.id = p.author_id
                WHERE p.id = :post_id
            """
            cursor.execute(query, {"post_id": post_id})
        post = cursor.fetchone()

    if post is None:
        return None
    post = dict(post)
    return post


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
