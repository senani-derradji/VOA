import pytest, os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.user import UserModel
from app.core.security import get_password_hash


db_path = "./TEST_VOA_SECRETS_MANAGER.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if os.path.exists(db_path):
    os.remove(db_path)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    admin = UserModel(
        username="admin", 
        password=get_password_hash("admin"), 
        role="admin")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()

    dev = UserModel(username="dev", password=get_password_hash("dev"), role="developer")
    db.add(dev)
    db.commit()
    db.refresh(dev)
    db.close()

db()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_headers_admin(client):
    resp = client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_dev(client):
    resp = client.post("/api/v1/auth/login", data={"username": "dev", "password": "dev"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
