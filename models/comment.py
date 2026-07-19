import sqlite3
from database.db import get_connection
from models.post import get_post

'''
1) Выдать комментарии к посту get_comments_for_post
2) Выдать комментарий get_comment
3) Создать комментарий к посту add_comment
4) Изменить комментарий к посту update_comment
5) Удалить комментарий к посту delete_comment
6) Скрыть комментарий к посту hide_comment
'''

def get_comments_for_post(user, post_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.*, u.username, u.avatar
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
    post = get_post(post_id)

    if user is None or user["role"] == "user" and post["author_id"] != user["id"]:
        comments = [c for c in comments if not c["is_hidden"]]

    return comments

def get_comment(comment_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM comments WHERE id = ?",
        (comment_id,)
    )
    comment = cursor.fetchone()

    conn.close()
    return comment

def add_comment(user_id, post_id, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO comments (post_id, author_id, content) VALUES (?, ?, ?)",
        (post_id, user_id, content),
    )
    conn.commit()
    conn.close()

def update_comment(comment_id, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE comments SET content = ? WHERE id = ?",
        (content, comment_id),
    )
    conn.commit()
    conn.close()

def delete_comment(comment_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM comments WHERE id = ?",
        (comment_id,)
    )
    conn.commit()
    conn.close()

def hide_comment(comment_id):
    conn = get_connection()
    cursor = conn.cursor()
    comment = get_comment(comment_id)
    is_hidden = 0 if comment["is_hidden"] == 1 else 1

    cursor.execute("UPDATE comments SET is_hidden = ? WHERE id = ?", (is_hidden, comment_id))
    conn.commit()
    conn.close()