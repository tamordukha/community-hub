# Community Hub

A social platform built with Flask featuring user roles, a permission system, comments, replies, likes, and avatars.

## Features

- **Three roles:** user, moderator, admin
- **Posts:** public and private, create, edit, delete
- **Comments:** create, edit, delete, hide
- **Replies:** to comments and to other replies (nested)
- **Likes:** posts, comments, replies (with AJAX updates)
- **Avatars:** upload and display
- **Comment sorting:** popular / recent
- **User profiles** with author posts
- **CSRF protection** on all forms
- **Tests:** pytest for auth, posts, comments, replies, likes, visibility

## Stack

- Python 3
- Flask
- Jinja2
- SQLite
- Flask-WTF (CSRF)
- JavaScript (AJAX for likes)
- pytest

## Installation

```bash
git clone <url>
cd community-hub
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running
```bash
flask run
```
or
```bash
python app.py
```

## Tests
```bash
pytest tests/ -v
```

## Structure
```text
community-hub/
├── app.py              # Entry point, Flask app factory
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
├── README.md           # This file
│
├── database/
│   ├── __init__.py
│   ├── db.py           # Database connection and initialization
│   └── schema.sql      # SQL tables schema
│
├── models/
│   ├── __init__.py
│   ├── user.py         # User model
│   ├── post.py         # Post model
│   ├── comment.py      # Comment model
│   ├── reply.py        # Reply model
│   └── like.py         # Like model
│
├── routes/
│   ├── __init__.py
│   ├── auth.py         # Register, login, logout
│   ├── posts.py        # Posts CRUD
│   ├── comments.py     # Comments CRUD
│   ├── replies.py      # Replies CRUD
│   ├── likes.py        # Like toggling
│   └── profile.py      # User profiles
│
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # Feed page
│   ├── auth/           # Login and register
│   ├── posts/          # Post pages
│   └── profile/        # Profile pages
│
├── static/
│   ├── css/            # Styles
│   ├── js/             # JavaScript files
│   ├── icons/          # UI icons
│   └── uploads/        # User avatars
│
├── utils/
│   ├── __init__.py
│   └── permissions.py  # Access control logic
│
└── tests/
    ├── __init__.py
    ├── conftest.py     # Pytest fixtures
    ├── test_auth.py
    ├── test_posts.py
    ├── test_comments.py
    ├── test_replies.py
    ├── test_likes.py
    └── test_visibility.py
```

## Deployment
```bash
gunicorn app:app
```

## Deployment
```bash
gunicorn app:app
```
