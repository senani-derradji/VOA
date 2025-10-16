import os, sys
from dotenv import load_dotenv
from string import Template


backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(backend_dir)

load_dotenv()

class Settings:
    raw_db_url = os.getenv("DATABASE_URL", "sqlite://./SMA.db")
    DATABASE_URL = Template(raw_db_url).substitute(
        USER=os.getenv("DB_USER", "derradji"),
        HOST=os.getenv("DB_HOST", "localhost"),
        PASSWORD=os.getenv("DB_PASSWORD", "derradji")
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "derradji_senani")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

settings = Settings()

# print(settings.DATABASE_URL)
# print(settings.SECRET_KEY)
# print(settings.ALGORITHM)
# print(settings.ACCESS_TOKEN_EXPIRE_MINUTES)