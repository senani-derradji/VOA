from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import auth, secrets
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging
from fastapi import Request


app = FastAPI(title="VOA : VAULITY OPS API",
              description="Secrets Manager API",
              version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

logger = logging.getLogger("blocked_ips")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("blocked_ips.log")
formatter = logging.Formatter("%(asctime)s - Blocked IP: %(message)s")
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    ip_address = request.client.host
    logger.warning(ip_address)
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Try again later."}
    )


app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("app/static/index.html")



app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(secrets.router, prefix="/api/v1/secrets", tags=["Secrets"])