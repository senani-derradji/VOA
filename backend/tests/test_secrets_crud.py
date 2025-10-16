from tests.utils import create_secret
from tests.conftest import random_name


def test_create_secret(client, auth_headers_dev):
    resp = create_secret(client, auth_headers_dev)
    assert resp.status_code == 200
    assert "secret_id" in resp.json()

def test_get_all_secrets(client, auth_headers_dev):
    resp = client.get("/api/v1/secrets/", headers=auth_headers_dev)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_secret_by_owner(client, auth_headers_dev):

    resp = create_secret(client, auth_headers_dev, name=f"my_secret")
    secret_id = resp.json()["secret_id"]

    resp = client.get(f"/api/v1/secrets/{secret_id}", headers=auth_headers_dev)
    assert resp.status_code == 200
    assert resp.json()["name"] == "my_secret"

def test_update_secret(client, auth_headers_dev):
    resp = create_secret(client, auth_headers_dev, name=f"update_secret_{random_name}")
    secret_id = resp.json()["secret_id"]

    update_data = {"name": "updated", "value": "456", "environment": "production"}
    resp = client.put(f"/api/v1/secrets/{secret_id}", headers=auth_headers_dev, json=update_data)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Secret updated successfully"

def test_delete_secret_admin(client, auth_headers_admin):
    resp = create_secret(client, auth_headers_admin, name=f"delete_secret_{random_name}")
    secret_id = resp.json()["secret_id"]

    resp = client.delete(f"/api/v1/secrets/{secret_id}", headers=auth_headers_admin)
    assert resp.status_code == 200
