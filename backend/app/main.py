from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging
from fastapi import Request
from prometheus_fastapi_instrumentator import Instrumentator


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
    contact={
        "Github": "https://github.com/senani-derradji",
        "FullName": "Derradji Senani",
        "Email": "derradjisn@gmail.com"
    },
)



@app.get("/health")
def health_check():
    return {"status": "ok"}


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
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


instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    ip_address = request.client.host
    logger.warning(ip_address)
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Try again later."}
    )

# app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.include_router(api_router, prefix="/api/v1")