import os, time, requests, subprocess
from dotenv import load_dotenv
from pathlib import Path
from cryptography.fernet import Fernet

USE_SQLITE = True
ENABLE_REDIS = False
ENV_FILE_NAME = '.env.encrypted'

BASE_DIR = Path.cwd()
PATHS = {"BACKEND": BASE_DIR / "backend"}

KEY_PATH = PATHS["BACKEND"] / "app" / "core" / "keys"
KEY_PATH.mkdir(parents=True, exist_ok=True)

dek1_path = KEY_PATH / "DEK_KEY_1.key.enc"

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

def start_container(compose_file, service_name=None, build=False):
    cmd = ["docker", "compose", "-f", compose_file, "up", "-d"]
    if build:
        cmd.append("--build")
    if service_name:
        if isinstance(service_name, list):
            cmd.extend(service_name)
        else:
            cmd.append(service_name)
    subprocess.run(cmd, check=True)

def wait_for_kek_server(auth_token, retries=10, delay=2):
    load_dotenv()
    kek = None
    for _ in range(retries):
        try:
            r = requests.get(
                "https://127.0.0.1:5555/get_kek",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=2,
                verify=False
            )
            if r.status_code == 200:
                kek = r.json()["kek"]
                print("[+] KEK server is ready.")
                break
        except requests.exceptions.RequestException:
            print("[*] KEK server is not ready yet...")
            time.sleep(delay)
    if not kek:
        raise RuntimeError("KEK server did not respond in time.")
    return kek

def main():
    use_full_compose = input("Use full docker-compose (docker-compose.full.yml)? (y/n): ").strip().lower() == "y"
    compose_file = "docker-compose.full.yml" if use_full_compose else "docker-compose.min.yml"

    print("[*] Starting KEK server container...")
    start_container(compose_file, service_name="kek_server", build=True)

    load_dotenv()
    AUTH = os.getenv("SECRET_AUTH")
    if not AUTH:
        AUTH = input("Enter SECRET_AUTH: ").strip()
    if not AUTH:
        raise RuntimeError("SECRET_AUTH is missing.")

    kek = wait_for_kek_server(AUTH)
    with open("KEK_HOST_FILE.key", "w") as f:
        f.write(f"{time.time()} : {kek}")

    kek_fernet = Fernet(kek.encode())

    if not dek1_path.exists():
        dek1_plain = Fernet.generate_key()
        dek1_path.write_bytes(kek_fernet.encrypt(dek1_plain))
    dek1_plain = kek_fernet.decrypt(dek1_path.read_bytes())
    f_1 = Fernet(dek1_plain)

    for path in PATHS.values():
        path.mkdir(parents=True, exist_ok=True)
        env_path = path / ENV_FILE_NAME
        with env_path.open("w", encoding="utf-8") as file:
            for key, value in DATA.items():
                enc_key = f_1.encrypt(key.encode()).decode()
                enc_value = f_1.encrypt(value.encode()).decode()
                file.write(f"{enc_key}DERRADJI{enc_value}\n")
        print(f"[+] {env_path} created successfully.")

    print("WAIT ....")
    time.sleep(5)

    print("[*] Starting backend services...")
    start_container(compose_file, service_name=["backend", "nginx"])

if __name__ == "__main__":
    main()
