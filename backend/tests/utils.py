from conftest import random_name

def create_secret(client, headers, name=f"test_secret_{random_name}", value="123", env="dev"):
    response = client.post(
        "/api/v1/secrets/create",
        headers=headers,
        params={"name": name, "value": value, "env": env}
    )
    return response