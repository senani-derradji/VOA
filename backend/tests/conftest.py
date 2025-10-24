from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.user import UserModel
from app.core.security import get_password_hash
import random, string, pytest, os


random_name = ''.join(random.choices(string.ascii_lowercase, k=10))
db_path = f"./TEST_VOA_{random_name}.db"


TEST_DATABASE_URL = f"sqlite:///{db_path}"
DB_USER=os.getenv("DB_USER", "root")
DB_PASSWORD=os.getenv("DB_PASSWORD", "root")
DB_HOST=os.getenv("DB_HOST", "localhost")
DB_NAME=os.getenv("DB_NAME")


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine)

if os.path.exists(db_path):
    os.remove(db_path)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
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

dev = UserModel(
    username="dev", 
    password=get_password_hash("dev"), 
    role="developer")
db.add(dev)
db.commit()
db.refresh(dev)
db.close()

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