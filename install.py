import os

DIR = os.getcwd()
ENV_FILE = '.env'

PATHS = {
    "BACKEND": os.path.join(DIR, "backend"),
    "TESTS": os.path.join(DIR, "backend/tests"),
    "CLI": os.path.join(DIR, "cli"),
    "HERE": DIR
}

DATA = {
    "DB_USER": "derradji",
    "DB_PASSWORD": "derradji95",
    "DB_NAME": "SMV",
    "REDIS_HOST": "redis",
    "REDIS_PASSWORD": "0@192@300@53@3493@3.14",
    "REDIS_PORT": "6379",
    "REDIS_DB": "0",
    "DATABASE_URL": "postgresql://${DB_USER}:${DB_PASSWORD}@database:5432/${DB_NAME}",
    "SECRET_KEY": "OSJ7MD5T5O",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
}

for name, path in PATHS.items():
    os.makedirs(path, exist_ok=True)
    env_path = os.path.join(path, ENV_FILE)
    with open(env_path, "w") as file:
        for k, v in DATA.items():
            file.write(f"{k}={v}\n")
    print(f"{env_path} created successfully.")

