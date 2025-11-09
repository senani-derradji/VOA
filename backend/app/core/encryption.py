from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os, sys, base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.logging_logs import get_logger
from app.core.config import settings, backend_dir
from app.core.keys.kek_manager import get_kek

logger = get_logger(__name__)

SECRET_KEY = settings.get("SECRET_KEY")
# ENV_ENC_KEYS = ".env.enckeys"
password = SECRET_KEY.encode()

DATA_CRYPT_PASS = {
    "salt" : os.urandom(16),
    "length" : 32,
    "IV" : 200_000
}

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=DATA_CRYPT_PASS["length"],
    salt=DATA_CRYPT_PASS["salt"],
    iterations=DATA_CRYPT_PASS["IV"],
    backend=default_backend()
)

key_bytes = kdf.derive(password)
fernet_key = base64.urlsafe_b64encode(key_bytes)

kek = get_kek() if not None else ""
if not kek:
    raise ValueError("KEK is missing or invalid.")

f_kek = Fernet(kek)

try:
    with open(f"{backend_dir}/app/core/keys/DEK_KEY_1.key.enc","rb") as key_file_1:
        key_01 = f_kek.decrypt(key_file_1.read())

    # with open(f"{backend_dir}/app/core/keys/DEK_KEY_2.key.enc", "rb") as key_file_2:
    #     key_02 = f_kek.decrypt(key_file_2.read())

except Exception as e:
    logger.error(f"ERROR IN KEK: {key_01}")


logger.info(f"Fernet key: {key_01}")

fernet = Fernet(key_01)

def encrypt(value: str) -> str:
    try:
        return fernet.encrypt(value.encode()).decode()
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise

def decrypt(token: str) -> str:
    try:
        result = fernet.decrypt(token.encode())
        return result.decode()
    except InvalidToken:
        logger.error("Invalid decryption token or wrong key.")
        pass
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        pass