import pytest
import tempfile
import os
from app import create_app
from database.db import init_db
import database.db as db


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-key",
        "WTF_CSRF_ENABLED": False,
    })

    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    db.DATABASE_PATH = db_path

    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(app):
    client = app.test_client()
    client.post("/register", data={
        "username": "testuser",
        "password": "password123",
    })
    client.post("/login", data={
        "username": "testuser",
        "password": "password123",
    })
    return client

@pytest.fixture
def auth_foreign_client(app):
    client = app.test_client()
    client.post("/register", data={
        "username": "otheruser",
        "password": "password123",
    })
    client.post("/login", data={
        "username": "otheruser",
        "password": "password123",
    })
    return client


@pytest.fixture
def auth_mod_client(app):
    client = app.test_client()
    client.post("/register", data={
        "username": "moderator",
        "password": "mod123",
    })
    client.post("/login", data={
        "username": "moderator",
        "password": "mod123",
    })
    
    # Меняем роль напрямую в БД
    conn = db.get_connection()
    conn.execute("UPDATE users SET role = 'moderator' WHERE username = 'moderator'")
    conn.commit()
    conn.close()
    
    # Обновляем сессию
    with client.session_transaction() as sess:
        sess["role"] = "moderator"
    
    return client

@pytest.fixture
def auth_admin_client(app):
    client = app.test_client()
    client.post("/register", data={
        "username": "admin",
        "password": "admin123",
    })
    client.post("/login", data={
        "username": "admin",
        "password": "admin123",
    })
    
    # Меняем роль напрямую в БД
    conn = db.get_connection()
    conn.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
    conn.commit()
    conn.close()
    
    # Обновляем сессию
    with client.session_transaction() as sess:
        sess["role"] = "admin"
    
    return client