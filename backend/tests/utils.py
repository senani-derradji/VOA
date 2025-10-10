import random
import string

def create_secret(client, headers, name="test_secret", value="123", env="dev"):
    response = client.post(
        "/api/v1/secrets/create",
        headers=headers,
        params={"name": name, "value": value, "env": env}
    )
    return response

# def name_not_exist(num : int = 10):
#     random_name = ''.join(random.choices(string.ascii_lowercase, k=num))
#     return random_name

