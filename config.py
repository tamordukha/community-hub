import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASEDIR, 'community.db')}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASEDIR, "static", "uploads", "avatars")

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    POST_MAX_LENGTH = 2000
    COMMENT_MAX_LENGTH = 500
    REPLY_MAX_LENGTH = 500