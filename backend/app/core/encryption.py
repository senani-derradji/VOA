from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os, sys, base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.logging_logs import get_logger
from app.core.config import settings, backend_dir
# sys.path.append(backend_dir)



logger = get_logger(__name__)

SECRET_KEY = settings.SECRET_KEY
ENV_ENC_KEYS = ".env.enckeys"
print(SECRET_KEY)
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

try :
    with open(f"{backend_dir}/app/core/keys/DEK_KEYS.key","r") as key:
        key_01 = key.readline().strip()
        key_02 = key.readline().strip()
except NameError as e:
    logger.error(f"ERROR IN ENCRYPTION KEYS:{e}")
    exit()

KEY_FILE_ENC =f"{backend_dir}/{ENV_ENC_KEYS}"
if not os.path.exists(KEY_FILE_ENC):
    with open(KEY_FILE_ENC,"w") as key_encryption:
        f = Fernet(key_01)
        for key, value in DATA_CRYPT_PASS.items():
            key_encryption.write(f"{key}DERRADJI{f.encrypt(str(value).encode()).decode()}\n")

with open(KEY_FILE_ENC,"r") as key_decryption:
    DATA_DECRYPT_PASS = {}
    for line in key_decryption.readlines():
        f = Fernet(key_01)
        try:
            key, value = line.strip().split("DERRADJI")
            DATA_DECRYPT_PASS[key] = f.decrypt(value.encode()).decode()
        except Exception as e:
            logger.error(f"ERROR IN DECRYPTION KEYS: {e}")


for key, value in DATA_DECRYPT_PASS.items():
    print(f"{key}: {value}")

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
