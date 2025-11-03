import random, string, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.encryption import encrypt
from app.utils.logging_logs import get_logger

# salt = DATA_CRYPT_PASS["salt"]
# fernet_key = key_01


logger = get_logger(__name__)

random_number = random.randint(15, 20)

def generate_random_word(length=16):
    data = ''.join(random.choices(string.ascii_lowercase, k=length))
    return encrypt(data)