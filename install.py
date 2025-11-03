from pathlib import Path
from cryptography.fernet import Fernet
import os

USE_SQLITE = True
ENABLE_REDIS = False

BASE_DIR = Path.cwd()
ENV_FILE_NAME = ".env.encrypted"

PATHS = {
    "BACKEND": BASE_DIR / "backend",
    "CLI": BASE_DIR / "cli",
    "HERE": BASE_DIR
}

KEY_PATH = PATHS["BACKEND"] / "app/core/keys"
KEY_PATH.mkdir(parents=True, exist_ok=True)

DATA = {
    "USE_SQLITE": str(USE_SQLITE).lower(),
    "ENABLE_REDIS": str(ENABLE_REDIS).lower(),
    "DB_USER": "derradji",
    "DB_PASSWORD": "derradji95",
    "DB_NAME": "SMV",
    "DB_HOST": "database",
    "DB_PORT": "5432",
    "DB_PATH": "./VOA.db",
    "DATABASE_URL": "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}",
    "REDIS_HOST": "redis",
    "REDIS_PORT": "6379",
    "REDIS_PASSWORD": "0@192@300@53@3493@3.14",
    "REDIS_DB": "0",
    "REDIS_ADDR": "${REDIS_HOST}:${REDIS_PORT}",
    "SECRET_KEY": "OSJ7MD5T",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
}

key_file_path = KEY_PATH / "DEK_KEYS.key"
if not key_file_path.exists():
    key_01 = Fernet.generate_key()
    key_02 = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key_01 + b"\n" + key_02)
else:
    with open(key_file_path, "rb") as key_file:
        key_01 = key_file.readline().strip()
        key_02 = key_file.readline().strip()

f_1 = Fernet(key_01)
f_2 = Fernet(key_02)


for name, path in PATHS.items():
    path.mkdir(parents=True, exist_ok=True)
    env_path = path / ENV_FILE_NAME

    try:
        with env_path.open("w", encoding="utf-8") as file:
            for key, value in DATA.items():
                encrypted_key = f_1.encrypt(key.encode()).decode()
                encrypted_value = f_1.encrypt(value.encode()).decode()
                file.write(f"{encrypted_key}DERRADJI{encrypted_value}\n")
        print(f"[+] {env_path} created successfully.")
    except Exception as e:
        print(f"[!] Failed to create {env_path}: {e}")

try:
    with env_path.open("r") as file:
        for line in file:
            if "DERRADJI" in line:
                enc_key, enc_value = line.strip().split("DERRADJI", 1)

                dec_key = f_1.decrypt(enc_key.encode()).decode()
                dec_value = f_1.decrypt(enc_value.encode()).decode()
                print(f"{dec_key}={dec_value}")
except Exception as e:
    print(f"[!] Failed to decrypt {env_path}: {e}")