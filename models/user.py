import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_connection


def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists", 400
    finally:
        conn.close()

    # Возвращаем созданного пользователя
    return get_user_by_username(username)


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    if check_password_hash(user["password"], password):
        return dict(user)

    return None


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None

def update_user_avatar(user_id, filename):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET avatar = ? WHERE id = ?", (filename, user_id),)
    conn.commit()
    conn.close()

def update_user_role(user_id, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id),)
    conn.commit()
    conn.close()