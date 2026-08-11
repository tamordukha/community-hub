def test_reply(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })
    auth_client.post("/post/1/comment/create", data={
        "content": "test comment create"
    })
    response = auth_client.post("/post/1/1/reply/create", data={
        "content": "test reply create"
    })
    assert response.status_code == 302
    assert "/post/1" in response.headers["Location"]

def test_reply_to_reply(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })
    auth_client.post("/post/1/comment/create", data={
        "content": "test comment create"
    })
    auth_client.post("/post/1/1/reply/create", data={
        "content": "test reply create"
    })
    response = auth_client.post("/post/1/1/reply/1/reply-to-reply", data={
        "content": "test reply to reply"
    })
    assert response.status_code == 302
    assert "/post/1" in response.headers["Location"]

def test_cannot_reply_when_guest(client, auth_client):
    auth_client.post("/post/create", data={
            "title": "Test post",
            "content": "Test content",
            "is_public": 1,
        })
    auth_client.post("/post/1/comment/create", data={
        "title": "Test",
        "content": "Content",
    })
    response = client.post("/post/1/1/reply/create", data={
        "content": "test reply create for guest"
    })

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]