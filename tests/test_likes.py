def test_toggle_like_post(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })

    auth_client.post("/post/like", data={"post_id": 1})
    response = auth_client.get("/post/1")
    assert response.status_code == 200
    assert b"like_active.png" in response.data
    
    auth_client.post("/post/like", data={"post_id": 1})
    response = auth_client.get("/post/1")
    assert response.status_code == 200
    assert b"like_inactive.png" in response.data

def test_toggle_like_comment(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })
    auth_client.post("/post/1/comment/create", data={
        "content": "Test content",
    })

    auth_client.post("/comment/like", data={"post_id": 1,"comment_id": 1})
    response = auth_client.get("/post/1")
    assert response.status_code == 200
    assert b"like_active.png" in response.data

    auth_client.post("/comment/like", data={"post_id": 1,"comment_id": 1})
    response = auth_client.get("/post/1")
    assert response.status_code == 200
    assert b"like_inactive.png" in response.data

def test_toggle_like_reply(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })
    auth_client.post("/post/1/comment/create", data={
        "content": "Test content",
    })
    auth_client.post("/post/1/1/reply/create", data={
        "content": "Test content",
    })

    auth_client.post("/reply/like", data={"post_id": 1,"reply_id": 1})
    response = auth_client.get("/post/1")
    assert response.status_code == 200
    assert b"like_active.png" in response.data

    auth_client.post("/reply/like", data={"post_id": 1,"reply_id": 1})
    response = auth_client.get("/post/1")
    assert response.status_code == 200
    assert b"like_inactive.png" in response.data