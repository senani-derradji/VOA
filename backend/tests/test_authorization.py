from tests.utils import create_secret

def test_dev_cannot_delete_other_secret(client, auth_headers_admin, auth_headers_dev):

    resp = create_secret(client, auth_headers_admin, name="admin_secret")
    secret_id = resp.json()["secret_id"]

    resp = client.delete(f"/api/v1/secrets/{secret_id}", headers=auth_headers_dev)
    assert resp.status_code == 403

def test_dev_cannot_view_other_secret(client, auth_headers_admin, auth_headers_dev):
    resp = create_secret(client, auth_headers_admin, name="admin_secret2")
    secret_id = resp.json()["secret_id"]

    resp = client.get(f"/api/v1/secrets/{secret_id}", headers=auth_headers_dev)
    assert resp.status_code == 403
