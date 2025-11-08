import requests, os #, ctypes
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)

KEK_SERVER = os.getenv("KEK_SERVER")
AUTH_TOKEN = os.getenv("SECRET_AUTH")

def get_kek():
    try:
        response = requests.get(
            KEK_SERVER,
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            timeout=5,
            verify=False # CHANGE IN PROD
        )
        response.raise_for_status()
        kek = response.json()["kek"].encode()
        return kek
    except Exception as e:
        logger.error("ERROR IN KEK MANAGER :",e)
        exit()