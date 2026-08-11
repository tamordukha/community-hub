def test_create_comment(auth_client):
    auth_client.post("/post/create", data={
        "title": "Test post",
        "content": "Test content",
        "is_public": 1,
    })
    response = auth_client.post("/post/1/comment/create", data={
        "content": "test comment create"
    })
    assert response.status_code == 302



def test_cannot_create_comment_when_guest(client, auth_client):
    auth_client.post("/post/create", data={
            "title": "Test post",
            "content": "Test content",
            "is_public": 1,
        })
    response = client.post("/post/1/comment/create", data={
        "title": "Test",
        "content": "Content",
    })

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_edit_comment(auth_client):
    create_resp = auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)
    
    auth_client.post("/post/1/comment/create", data={
            "content": "test comment create"
        })
    
    response = auth_client.post("/post/1/comment/1/edit", data={
        "content": "Edited comment",
    })
    assert response.status_code == 302


def test_cannot_edit_comment_when_another_user(auth_client, auth_foreign_client):
    # Создаём пост и комментарий
    auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)

    create_resp = auth_client.post("/post/1/comment/create", data={
            "content": "comment create"
        }, follow_redirects=True)

    # Редактируем
    response = auth_foreign_client.post("/post/1/comment/1/edit", data={
        "content": "Edited comment",
    })
    
    assert response.status_code == 403


def test_delete_comment(auth_client):
    auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)
    
    create_resp = auth_client.post("/post/1/comment/create", data={
        "content": "comment create"
    }, follow_redirects=True)

    response = auth_client.post("/post/1/comment/1/delete")

    assert response.status_code == 302


def test_can_moderator_delete_foreign_comment(auth_mod_client, auth_client):
    auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)
    
    create_resp = auth_client.post("/post/1/comment/create", data={
        "content": "comment create"
    }, follow_redirects=True)

    response = auth_mod_client.post("/post/1/comment/1/delete")
    
    assert response.status_code == 302

def test_can_admin_edit_foreign_comment(auth_admin_client, auth_client):
    auth_client.post("/post/create", data={
        "title": "Original",
        "content": "Original content",
        "is_public": 1,
    }, follow_redirects=True)
    
    create_resp = auth_client.post("/post/1/comment/create", data={
        "content": "comment create"
    }, follow_redirects=True)

    response = auth_admin_client.post("/post/1/comment/1/edit", data={
        "content": "Edited comment by admin",
    })
    
    assert response.status_code == 302

