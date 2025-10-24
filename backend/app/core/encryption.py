from cryptography.fernet import Fernet
import base64
from app.core.security import SEC_KEY

key = base64.urlsafe_b64encode(SEC_KEY.encode().ljust(32, b'0'))

fernet = Fernet(key)

def encrypt(value: str) -> str:
    encrypted_value = fernet.encrypt(value.encode())
    return base64.urlsafe_b64encode(encrypted_value).decode()


def decrypt(value: str) -> str:
    encrypted_value = base64.urlsafe_b64decode(value)
    decrypted_value = fernet.decrypt(encrypted_value)
    return decrypted_value.decode()