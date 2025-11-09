import os, sys
from cryptography.fernet import Fernet
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)

defaults = {
    "HOST": "localhost",
    "USER": "user",
    "PASSWORD": "password"
}

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(backend_dir)

from app.core.keys.kek_manager import get_kek

ENV_FILE_NAME = ".env.encrypted"

try:
    kek = get_kek() if not None else ""
    if not kek: raise ValueError("KEK is missing or invalid.")
    f_kek = Fernet(kek)
except Exception as e:
    logger.error(f"ERROR IN KEK: {e}")
    sys.exit(1)

try:
    with open(f"{backend_dir}/app/core/keys/dek.key.enc", "rb") as key_file_1:
        key_01 = f_kek.decrypt(key_file_1.read())
except Exception as e:
    logger.error(f"ERROR IN dek.key: {e}")
    key_01 = None

if not key_01:
    raise RuntimeError("dek.key could not be decrypted.")

class Settings:
    def __init__(self, env_path, dek):
        self.data = {}
        f_dek = Fernet(dek)
        try:
            with open(env_path, "rb") as file:
                lines = file.readlines()
                for line in lines:
                    if not line.strip():
                        continue
                    if b"DERRADJI" not in line:
                        continue
                    key, value = line.strip().split(b"DERRADJI")
                    decrypted_key = f_dek.decrypt(key).decode()
                    decrypted_value = f_dek.decrypt(value).decode()
                    self.data[decrypted_key] = decrypted_value
        except Exception as e:
            logger.error(f"Error loading environment variables: {e}")


    def get(self, key, default=None):
        return self.data.get(key, default)

settings = Settings(f"{backend_dir}/{ENV_FILE_NAME}", key_01)
