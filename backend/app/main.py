from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import asyncio, logging, os, sys
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator

from app.extentions.database import SessionLocal
from app.models.secrets import SecretsModel
from app.models.user import UserModel
from app.services.check_TTL import check_TTL
from app.core.verify_integrity import verify
from app.core.keys.kek_manager import get_kek, update_kek

# Metadata
tags_metadata = [
    {"name": "Auth", "description": "Authentication and token operations."},
    {"name": "Users", "description": "User registration and management."},
    {"name": "Secrets", "description": "CRUD operations for secrets."},
    {"name": "Logs", "description": "Access and manage audit logs."},
]

app = FastAPI(
    title="VOA : VAULITY OPS API",
    description="Secrets Manager API for secure credential and secret management.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
logger = logging.getLogger("backend")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("backend.log")
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(file_handler)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests."})

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Include API routes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.api.api import api_router
app.include_router(api_router, prefix="/api/v1")

# Background tasks (TTL + DEK rotation)
async def ttl_background_task():
    while True:
        db: Session = SessionLocal()
        try:
            check_TTL(db, SecretsModel, "secret")
            check_TTL(db, UserModel, "user")
            verify(db)
        except Exception as e:
            logger.error(f"Error in TTL background task: {e}")
        finally:
            db.close()
        await asyncio.sleep(30)

DEK_PATH = "app/core/keys/dek.key.enc"

def load_dek():
    kek = get_kek()
    f = Fernet(kek)
    if os.path.exists(DEK_PATH):
        enc_dek = open(DEK_PATH, "rb").read()
        dek = f.decrypt(enc_dek)
        return dek
    else:
        dek = Fernet.generate_key()
        enc_dek = f.encrypt(dek)
        with open(DEK_PATH, "wb") as f_out:
            f_out.write(enc_dek)
        logger.info("New DEK created.")
        return dek

def rotate_dek():
    kek = get_kek()
    f_kek = Fernet(kek)
    if not os.path.exists(DEK_PATH):
        old_dek = Fernet.generate_key()
    else:
        enc_old_dek = open(DEK_PATH, "rb").read()
        old_dek = f_kek.decrypt(enc_old_dek)

    new_dek = Fernet.generate_key()
    enc_new_dek = f_kek.encrypt(new_dek)
    with open(DEK_PATH, "wb") as f_out:
        f_out.write(enc_new_dek)

    db = SessionLocal()
    try:
        secrets = db.query(SecretsModel).all()
        f_old = Fernet(old_dek)
        f_new = Fernet(new_dek)
        for secret in secrets:
            decrypted = f_old.decrypt(secret.value.encode())
            secret.value = f_new.encrypt(decrypted).decode()
        db.commit()
        logger.info("DEK rotation completed.")
    except Exception as e:
        db.rollback()
        logger.error(f"DEK rotation failed: {e}")
    finally:
        db.close()

async def dek_rotation_task():
    while True:
        try:
            rotate_dek()
        except Exception as e:
            logger.error(f"Error rotating DEK: {e}")
        await asyncio.sleep(12 * 60 * 60)

# ✅ Webhook endpoint for KEK update
@app.post("/update-kek")
async def update_kek_endpoint(request: Request):
    data = await request.json()
    secret_header = request.headers.get("X-Auth-Token")
    expected_secret = os.getenv("BACKEND_SECRET", "super_secret_shared_token")
    if secret_header != expected_secret:
        return JSONResponse(status_code=403, content={"detail": "Forbidden"})

    new_kek = data.get("kek")
    if not new_kek:
        return JSONResponse(status_code=400, content={"detail": "Missing KEK"})
    update_kek(new_kek)
    return {"status": "KEK updated successfully"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(ttl_background_task())
    asyncio.create_task(dek_rotation_task())
    logger.info("Background tasks started.")
