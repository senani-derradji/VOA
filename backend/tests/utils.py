def create_secret(client, headers, name="test_secret", value="123", env="dev"):
    response = client.post(
        "/api/v1/secrets/create",
        headers=headers,
        params={"name": name, "value": value, "env": env}
    )
    return response