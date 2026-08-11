def test_guest_cannot_see_private_posts(auth_client, client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 0,
    })
    response = client.get("/")
    assert b"post-status" not in response.data

def test_user_can_see_their_private_posts(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 0,
    })
    response = auth_client.get("/")
    assert b"post-status" in response.data

def test_user_cannot_see_foreign_private_posts(auth_client, auth_foreign_client):
    auth_foreign_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 0,
    })
    response = auth_client.get("/")
    assert b"post-status" not in response.data

def test_mod_can_see_foreign_private_posts(auth_client, auth_mod_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 0,
    })
    response = auth_mod_client.get("/")
    assert b"post-status" in response.data

def test_admin_can_see_foreign_private_posts(auth_client, auth_admin_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 0,
    })
    response = auth_admin_client.get("/")
    assert b"post-status" in response.data