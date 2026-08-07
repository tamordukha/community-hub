from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import register_user, login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_template(
                "auth/register.html", error="Username and password are required"
            )

        user = register_user(username, password, "user")
        if user is None:
            return render_template(
                "auth/register.html", error="Username already exists"
            )

        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_template(
                "auth/login.html", error="Username and password are required"
            )

        user = login_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["avatar"] = user["avatar"]
            return redirect(url_for("posts.index"))

        return render_template("auth/login.html", error="Incorrect username or password")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))