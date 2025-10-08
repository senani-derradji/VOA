import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    
    def __init__(self):
        print(f"   DATABASE_URL: {self.DATABASE_URL}")
        print(f"   SECRET_KEY: {'*' * len(self.SECRET_KEY) if self.SECRET_KEY else 'None'}")
        print(f"   ALGORITHM: {self.ALGORITHM}")
        print(f"   ACCESS_TOKEN_EXPIRE_MINUTES: {self.ACCESS_TOKEN_EXPIRE_MINUTES}")

settings = Settings()