from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os, sys, base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.logging_logs import get_logger
from app.core.config import settings



logger = get_logger(__name__)

SECRET_KEY = settings.SECRET_KEY
print(SECRET_KEY)
password = SECRET_KEY.encode()

salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=200_000,
    backend=default_backend()
)

key_bytes = kdf.derive(password)
fernet_key = base64.urlsafe_b64encode(key_bytes)
logger.info(f"Fernet key: {fernet_key}")


fernet = Fernet(fernet_key)


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
