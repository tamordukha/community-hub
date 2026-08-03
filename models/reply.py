import sqlite3
from collections import defaultdict
from database.db import get_connection
from models.post import get_post 
from models.comment import get_comment
from models.user import get_user_by_id

'''
1) Выдать ответы в виде журнала {comment_id:[ответы],} к посту get_replies_for_post
    replies = {
        1:[{"comment_id":1, "content": "lala"}, {"comment_id":1, "content": "horse"}],
        2:[{"comment_id":2, "content": "aaaa"}, {"comment_id":2, "content": "llalalal"}]
    }
2) Выдать ответ get_reply
3) Создать ответ к комментарию add_reply
4) Создать ответ к ответу add_reply_to_reply
5) Изменить ответ update_reply
6) Удалить ответ delete_reply
7) Скрыть ответ hide_reply
8) Выдать число ответов get_replies_count
'''

def get_replies_for_post(post_id, user=None):
    conn = get_connection()
    cursor = conn.cursor()

    if user:
        cursor.execute(
            """
            SELECT
                r.*, u.username, u.avatar,
                (SELECT COUNT(*) FROM reply_likes WHERE reply_id = r.id) AS like_count,
                (SELECT COUNT(*) FROM reply_likes WHERE reply_id = r.id AND user_id = :user_id) AS liked_by_current_user
            FROM replies r
            JOIN users u ON u.id = r.author_id
            JOIN comments c ON r.comment_id = c.id
            WHERE c.post_id = :post_id
            ORDER BY c.created_at ASC
            """,
            {"post_id": post_id, "user_id": user["id"]}
        )

    else:
        cursor.execute(
            """
            SELECT
                r.*, u.username, u.avatar,
                (SELECT COUNT(*) FROM reply_likes WHERE reply_id = r.id) AS like_count
            FROM replies r
            JOIN users u ON u.id = r.author_id
            JOIN comments c ON r.comment_id = c.id
            WHERE c.post_id = :post_id
            ORDER BY c.created_at ASC
            """,
            {"post_id": post_id}
        )

    replies = cursor.fetchall()
    conn.close()

    replies = [dict(r) for r in replies]
    post = get_post(post_id)

    if user is None or user["role"] == "user" and post["author_id"] != user["id"]:
        replies = [r for r in replies if not r["is_hidden"]]

    dict_replies = defaultdict(list,{})
    for r in replies:
        comment_id = r["comment_id"]
        if r["parent_reply_id"]:
            parent_reply = get_reply(r["parent_reply_id"])
            parent_reply_user = get_user_by_id(parent_reply["author_id"])
            parent_reply_username = parent_reply_user["username"]
            r["parent_reply_username"] = parent_reply_username
        dict_replies[comment_id].append(r)

    replies = dict_replies
    return replies

def get_reply(reply_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM replies WHERE id = ?",
        (reply_id,)
    )
    reply = cursor.fetchone()

    conn.close()
    return reply

def add_reply(user_id, comment_id, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO replies (comment_id, author_id, content) VALUES (?, ?, ?)",
        (comment_id, user_id, content),
    )
    conn.commit()
    conn.close()

def add_reply_to_reply(user_id, comment_id, parent_reply_id, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO replies (comment_id, parent_reply_id, author_id, content) VALUES (?, ?, ?, ?)",
        (comment_id, parent_reply_id, user_id, content),
    )
    conn.commit()
    conn.close()

def update_reply(reply_id, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE replies SET content = ? WHERE id = ?",
        (content, reply_id),
    )
    conn.commit()
    conn.close()

def delete_reply(reply_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM replies WHERE id = ?",
        (reply_id,)
    )
    conn.commit()
    conn.close()

def hide_reply(reply_id):
    conn = get_connection()
    cursor = conn.cursor()
    reply = get_reply(reply_id)
    is_hidden = 0 if reply["is_hidden"] == 1 else 1

    cursor.execute("UPDATE replies SET is_hidden = ? WHERE id = ?", (is_hidden, reply_id))
    conn.commit()
    conn.close()

def get_replies_count(user, post_id):
    replies = get_replies_for_post(post_id, user)
    replies_count = {}
    
    for comment_id, list_replies in replies.items():
        replies_count[comment_id] = len(list_replies)

    return replies_count