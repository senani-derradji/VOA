from pathlib import Path
from datetime import datetime

USE_SQLITE = True
ENABLE_REDIS = not (USE_SQLITE)

BASE_DIR = Path.cwd()
ENV_FILE_NAME = ".env"

PATHS = {
    "BACKEND": BASE_DIR / "backend",
    "CLI": BASE_DIR / "cli",
    "HERE": BASE_DIR
}

DATA = {
    "CREATED_AT": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "USE_SQLITE": str(USE_SQLITE).lower(),
    "ENABLE_REDIS": str(ENABLE_REDIS).lower(),

    "DB_USER": "derradji",
    "DB_PASSWORD": "derradji95",
    "DB_NAME": "SMV",
    "DB_HOST": "database",
    "DB_PORT": "5432",
    "DB_PATH": "./SMA.db",
    "DATABASE_URL": "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}",

    "REDIS_HOST": "redis",
    "REDIS_PORT": "6379",
    "REDIS_PASSWORD": "0@192@300@53@3493@3.14",
    "REDIS_DB": "0",
    "REDIS_ADDR": "${REDIS_HOST}:${REDIS_PORT}",

    "SECRET_KEY": "OSJ7MD5T5O",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
}

for name, path in PATHS.items():
    path.mkdir(parents=True, exist_ok=True)
    env_path = path / ENV_FILE_NAME

    try:
        with env_path.open("w", encoding="utf-8") as file:
            for key, value in DATA.items():
                file.write(f"{key}={value}\n")
        print(f"[+] {env_path} created successfully.")
    except Exception as e:
        print(f"[!] Failed to create {env_path}: {e}")

print("\n=== Configuration Summary ===")
print(f"USE_SQLITE is {'ENABLED' if USE_SQLITE else 'DISABLED'}")
print(f"ENABLE_REDIS is {'ENABLED' if ENABLE_REDIS else 'DISABLED'}")
print(f"All .env files contain a creation date: {DATA['CREATED_AT']}")
print("=== End of Configuration Summary ===\n")