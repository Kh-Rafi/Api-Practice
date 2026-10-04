def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "newuser@test.com",
        "password": "pass123",
        "full_name": "New User",
        "role": "passenger"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert "password" not in data           # ⭐ password leak নেই
    assert "hashed_password" not in data    # ⭐ hash leak নেই


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "dup@test.com",
        "password": "pass123",
        "full_name": "First User"
    })
    response = client.post("/auth/register", json={
        "email": "dup@test.com",
        "password": "pass456",
        "full_name": "Second User"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "login@test.com",
        "password": "pass123",
        "full_name": "Login User"
    })
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "wrong@test.com",
        "password": "correct123",
        "full_name": "Wrong Pass"
    })
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401