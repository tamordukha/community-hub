import sqlite3
import os

from config import BASEDIR

DATABASE_PATH = os.path.join(BASEDIR, "community.db")
SCHEMA_PATH = os.path.join(BASEDIR, "database", "schema.sql")

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # чтобы можно было обращаться к полям по имени: row["username"]
    conn.execute("PRAGMA foreign_keys = ON")  # включаем поддержку внешних ключей
    return conn

def init_db():
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()

