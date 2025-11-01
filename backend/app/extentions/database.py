import os, sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(backend_dir)

load_dotenv()

from app.core.config import settings
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)

DATABASE_FULL = settings.DATABASE_URL.lower() != "false"
DATABASE_LITE = settings.DATABASE_LITE.lower() != "false"

sqlite_path = os.getenv("DB_PATH", "./VOA.db")

if DATABASE_LITE:
    logger.info("Using SQLite lite database")
    database_url = f"sqlite:///{sqlite_path}"

elif DATABASE_FULL:
    logger.info("Using full Postgres database")
    database_url = settings.DATABASE_URL

else:
    logger.error("No database configured in environment variables.")
    raise RuntimeError("Database not configured")

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
