from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, session, abort
import os
from models.post import get_posts
from models.user import get_user_by_id, update_user_avatar, update_user_role
from utils.permissions import can_change_role, can_modify_role

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile/<int:profile_user_id>", methods=["GET", "POST"])
def profile(profile_user_id):
    if session:
        current_user = {"id": session["user_id"], "role": session["role"]}
    else:
        current_user = None
    user = get_user_by_id(profile_user_id)
    posts = get_posts(user, profile_user_id)

    return render_template("profile/profile.html", current_user=current_user, user=user, posts=posts, can_modify_role=can_modify_role, can_change_role=can_change_role, how_bottom_bar=True)

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

@profile_bp.route("/role/<int:profile_user_id>", methods=["POST"])
def change_role(profile_user_id):
    if not session or session["role"]=="user":
        return redirect(url_for("profile.profile", profile_user_id=profile_user_id))
    
    current_user=get_user_by_id(session["user_id"])
    profile_user = get_user_by_id(profile_user_id)
    new_role = request.form.get("new_role")

    if can_change_role(current_user, profile_user, new_role):
        update_user_role(profile_user_id, new_role)
    else:
        abort(403)

    return redirect(url_for("profile.profile", profile_user_id=profile_user_id))