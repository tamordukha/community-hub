import sqlite3
from database.db import get_connection

'''
1) Лайк поста toggle_like_post
2) Лайк комментария toggle_like_comment
3) Лайк ответа toggle_like_reply
4) Подсчет лайков get_likes_count
'''

def toggle_like_post(post_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM post_likes WHERE user_id = ? AND post_id = ?",
        (user_id, post_id),
    )
    post_like_id = cursor.fetchone()

    if post_like_id:
        cursor.execute(
            "DELETE FROM post_likes WHERE user_id = ? AND post_id = ?",
            (user_id, post_id),
        )
    else:
        cursor.execute(
            "INSERT INTO post_likes (user_id, post_id) VALUES (?, ?)",
            (user_id, post_id),
        )
        
    conn.commit()
    conn.close()


def toggle_like_comment(comment_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM comment_likes WHERE user_id = ? AND comment_id = ?",
        (user_id, comment_id),
    )
    comment_like_id = cursor.fetchone()

    if comment_like_id:
        cursor.execute(
            "DELETE FROM comment_likes WHERE user_id = ? AND comment_id = ?",
            (user_id, comment_id),
        )
    else:
        cursor.execute(
            "INSERT INTO comment_likes (user_id, comment_id) VALUES (?, ?)",
            (user_id, comment_id),
        )
        
    conn.commit()
    conn.close()


def toggle_like_reply(reply_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM reply_likes WHERE user_id = ? AND reply_id = ?",
        (user_id, reply_id),
    )
    reply_like_id = cursor.fetchone()

    if reply_like_id:
        cursor.execute(
            "DELETE FROM reply_likes WHERE user_id = ? AND reply_id = ?",
            (user_id, reply_id),
        )
    else:
        cursor.execute(
            "INSERT INTO reply_likes (user_id, reply_id) VALUES (?, ?)",
            (user_id, reply_id),
        )
        
    conn.commit()
    conn.close()