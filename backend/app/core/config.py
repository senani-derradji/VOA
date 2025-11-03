import os, sys
from dotenv import load_dotenv

defaults = {
    "HOST": "localhost",
    "USER": "user",
    "PASSWORD": "password"
}

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(backend_dir)

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "false")
    DATABASE_LITE = os.getenv("USE_SQLITE", "false")

    REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", defaults["HOST"])
    REDIS_USERNAME = os.getenv("REDIS_USERNAME", defaults["USER"])
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", defaults["PASSWORD"])
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

    SECRET_KEY = os.getenv("SECRET_KEY", "derradji_senani")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

settings = Settings()
print(settings.SECRET_KEY)