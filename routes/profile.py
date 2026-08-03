from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort
import os
from models.post import get_posts
from models.user import get_user_by_id, update_user_avatar

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile/<int:profile_user_id>", methods=["GET", "POST"])
def profile(profile_user_id):

    user = get_user_by_id(profile_user_id)
    posts = get_posts(user, profile_user_id)

    return render_template("profile/profile.html", user=user, posts=posts, show_bottom_bar=True)

@profile_bp.route("/avatar/<int:profile_user_id>", methods=["POST"])
def update_avatar(profile_user_id):
    if "avatar" not in request.files:
        return redirect(url_for("profile.profile", profile_user_id=profile_user_id))

    file = request.files["avatar"]
    if file.filename == "":
        return redirect(url_for("profile.profile", profile_user_id=profile_user_id))
    
    filename = f"{session['user_id']}.jpg"
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    
    update_user_avatar(session["user_id"], filename)
    session['avatar'] = filename
    
    
    return redirect(url_for("profile.profile", profile_user_id=profile_user_id))