def test_register(client):
    response = client.post("/register", data={
        "username": "testuser",
        "password": "password123",
    })

    assert response.status_code == 302  # редирект на логин

def test_used_username(client):
    # Первая регистрация — успешная
    client.post("/register", data={
        "username": "testuser",
        "password": "password123",
    })
    
    # Вторая — имя занято
    response = client.post("/register", data={
        "username": "testuser",
        "password": "password123",
    })
    
    assert response.status_code == 200  # остаёмся на странице регистрации
    assert b"Username already exists" in response.data  # проверяем сообщение об ошибке
def test_login(client):
    # Сначала регистрируем
    client.post("/register", data={"username": "testuser", "password": "password123"})
    # Логинимся
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123",
    })
    assert response.status_code == 302  # редирект на ленту

def test_wrong_password(client):
    client.post("/register", data={"username": "testuser", "password": "password123"})
    response = client.post("/login", data={
        "username": "testuser",
        "password": "wrongpassword",
    })
    assert response.status_code == 200  # остаёмся на логине
    assert b"Incorrect" in response.data