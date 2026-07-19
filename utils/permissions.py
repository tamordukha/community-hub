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