from flask import Flask
from config import Config
from database.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db()

    register_routes(app)
    return app

def register_routes(app):
    from routes.auth import auth_bp
    from routes.posts import posts_bp
    from routes.comments import comments_bp
    from routes.replies import replies_bp
    from routes.likes import likes_bp
    #from routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(replies_bp)
    app.register_blueprint(likes_bp)
    #app.register_blueprint(profile_bp)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)