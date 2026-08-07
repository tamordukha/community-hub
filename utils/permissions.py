def can_view_post(user, post):
    if post["is_public"]:
        return True
    if user is None:
        return False
    if user["id"] == post["author_id"]:
        return True
    if user["role"] in ("moderator", "admin"):
        return True
    return False


def can_edit_post(user, post):
    if user is None:
        return False
    if user["id"] == post["author_id"]:
        return True
    if user["role"] == "admin":
        return True
    return False


def can_delete_post(user, post):
    if user is None:
        return False
    if user["id"] == post["author_id"]:
        return True
    if user["role"] in ("moderator", "admin"):
        return True
    return False


def can_edit_comment(user, comment):
    if user is None:
        return False
    if user["id"] == comment["author_id"]:
        return True
    if user["role"] == "admin":
        return True
    return False


def can_delete_comment(user, comment):
    if user is None:
        return False
    if user["id"] == comment["author_id"]:
        return True
    if user["role"] in ("moderator", "admin"):
        return True
    return False

def can_hide_comment(user, post, comment):
    if user is None or comment is None:
        return False
    if user["id"] == comment["author_id"]:
        return None
    if user["id"] == post["author_id"]:
        return True
    return user["role"] in ("moderator", "admin")


def can_edit_reply(user, reply):
    return can_edit_comment(user, reply)


def can_delete_reply(user, reply):
    return can_delete_comment(user, reply)


def can_hide_reply(user, post, reply):
    if user is None or reply is None:
        return False
    if user["id"] == reply["author_id"]:
        return None
    if user["id"] == post["author_id"]:
        return True
    return user["role"] in ("moderator", "admin")


def can_set_moderator(user):
    if user is None:
        return False
    return user["role"] in ("moderator", "admin")

def can_set_admin(user):
    if user is None:
        return False
    return user["role"] == "admin"


def can_change_role(current_user, profile_user, new_role):
    if current_user is None:
        return False
    if current_user["id"] == profile_user["id"] or profile_user["role"] == new_role:
        return False
    if current_user["role"]=="moderator" and profile_user["role"]=="user" and new_role=="moderator":
        return True
    if current_user["role"] == "admin" and profile_user["role"] != "admin":
        return True
    return False

def can_modify_role(current_user, profile_user):
    if current_user is None:
        return False
    if current_user["id"] == profile_user["id"]:
        return False
    if current_user["role"] == "admin" and profile_user["role"] != "admin":
        return True
    if current_user["role"] == "moderator" and profile_user["role"] == "user":
        return True
    return False