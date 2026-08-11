def test_create_post(auth_client):
    response = auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })
    assert response.status_code == 302


def test_cannot_create_post_when_guest(client):
    response = client.post("/post/create", data={
        "title": "Test",
        "content": "Content",
    })
    assert response.status_code == 302

def test_edit_post(auth_client):
    # Создаём пост
    create_resp = auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)
    
    # Редактируем
    response = auth_client.post("/post/edit/1", data={
        "title": "Edited",
        "content": "Edited content",
        "is_public": 0,
    })
    assert response.status_code == 302

def test_cannot_edit_post_when_another_user(auth_client, auth_foreign_client):
    # Создаём пост
    create_resp = auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)

    # Редактируем
    response = auth_foreign_client.post("/post/edit/1", data={
        "title": "Edited",
        "content": "Edited content",
        "is_public": 0,
    })
    print("Redirect to:", response.headers.get("Location"))
    resp = auth_foreign_client.get("/post/1")
    print("Foreign user can see post:", resp.status_code)
    
    assert response.status_code == 403