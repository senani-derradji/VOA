import os, sys, base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from app.utils.logging_logs import get_logger
from cryptography.fernet import InvalidToken

logger = get_logger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "derradji_senani")
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

fernet = Fernet(fernet_key)

def encrypt(value: str) -> str:
    try:
        return fernet.encrypt(value.encode()).decode()
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise

def decrypt(token: str) -> str:
    try:
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        logger.error("Invalid decryption token or wrong key.")
        raise
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise


print(encrypt("test"))
print(decrypt(encrypt("test")))