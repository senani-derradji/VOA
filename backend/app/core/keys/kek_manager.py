import requests, os, threading
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)

KEK_SERVER = os.getenv("KEK_SERVER")
AUTH_TOKEN = os.getenv("SECRET_AUTH")

current_kek = None
kek_lock = threading.Lock()

def fetch_kek():
    global current_kek
    try:
        response = requests.get(
            KEK_SERVER,
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            timeout=5,
            verify=False  # Change in production
        )
        response.raise_for_status()
        kek = response.json()["kek"].encode()
        with kek_lock:
            current_kek = kek
        logger.info("KEK fetched and stored successfully.")
        return kek
    except Exception as e:
        logger.error("ERROR IN KEK MANAGER:", e)
        exit()

def get_kek():
    with kek_lock:
        if current_kek:
            return current_kek
    return fetch_kek()

def update_kek(new_kek: str):
    global current_kek
    with kek_lock:
        current_kek = new_kek.encode()
    logger.info("KEK updated via webhook successfully.")
