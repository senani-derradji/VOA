def test_login_admin(client):
    response = client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_dev(client):
    response = client.post("/api/v1/auth/login", data={"username": "dev", "password": "dev"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_credentials_password(client):
    response = client.post("/api/v1/auth/login", data={"username": "dev", "password": "wrong"})
    assert response.status_code == 401

def test_login_wrong_credentials_username(client):
    response = client.post("/api/v1/auth/login", data={"username": "wrongUsername", "password": "wrong"})
    assert response.status_code != 200