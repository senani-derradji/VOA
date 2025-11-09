import os, time, requests
from dotenv import load_dotenv
from pathlib import Path
from cryptography.fernet import Fernet

USE_SQLITE = True
ENABLE_REDIS = False
ENV_FILE_NAME = '.env.encrypted'

BASE_DIR = Path.cwd()
PATHS = {
    "BACKEND": BASE_DIR / "backend",
    # "CLI": BASE_DIR / "cli"
}

KEY_PATH = PATHS["BACKEND"] / "app" / "core" / "keys"
KEY_PATH.mkdir(parents=True, exist_ok=True)

dek1_path = KEY_PATH / "DEK_KEY_1.key.enc"
dek2_path = KEY_PATH / "DEK_KEY_2.key.enc"

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

print("[*] Starting KEK server container...")
os.system("docker compose -f docker-compose.min.yml up -d kek_server --build")

print("[*] Waiting for KEK server to be ready...")
load_dotenv()
AUTH=os.getenv("SECRET_AUTH")
print(AUTH)
for i in range(10):
    try:
        r = requests.get(
            "https://127.0.0.1:5555/get_kek",
            headers={"Authorization": f"Bearer {AUTH}"},
            timeout=1,
            verify=False
        )

        if r.status_code == 200:
            kek = r.json()["kek"]
            print("[+] KEK server is ready.")
    except requests.exceptions.RequestException:
        print("[*] KEK server is not ready yet...")
        time.sleep(2)

print("======= kek =======")
print(kek)
print("===================")

kek_fernet = Fernet(kek.encode())
kek_host = "KEK_HOST_FILE.key"
with open(kek_host, "w") as f: f.write(f"{time.time()} : {kek}")

dek1_plain = Fernet.generate_key()
with open(dek1_path, "wb") as f: f.write(kek_fernet.encrypt(dek1_plain))
enc_dek1 = dek1_path.read_bytes()
key_01 = kek_fernet.decrypt(enc_dek1)
f_1 = Fernet(key_01)

# KEY 2 -----------------------------------------
# dek2_plain = Fernet.generate_key()
# with open(dek2_path, "wb") as f: f.write(kek_fernet.encrypt(dek2_plain))
# enc_dek2 = dek2_path.read_bytes()
# key_02 = kek_fernet.decrypt(enc_dek2)
# f_2 = Fernet(key_02)

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
        exit()

print("WAIT ....")
time.sleep(10)
os.system(f"cd {BASE_DIR} && docker compose -f docker-compose.min.yml up -d backend nginx")