import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models


# ═══════════════════════════════════════════
# Test Database (SQLite in-memory — fast!)
# ═══════════════════════════════════════════
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ═══════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════
@pytest.fixture(scope="function")
def db():
    """প্রতিটা test এর জন্য fresh database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """TestClient with overridden DB dependency"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    """Admin user create + login → token"""
    client.post("/auth/register", json={
        "email": "admin@test.com",
        "password": "admin123",
        "full_name": "Test Admin",
        "role": "admin"
    })
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    return response.json()["access_token"]


@pytest.fixture
def staff_token(client):
    """Staff user create + login → token"""
    client.post("/auth/register", json={
        "email": "staff@test.com",
        "password": "staff123",
        "full_name": "Test Staff",
        "role": "staff"
    })
    response = client.post("/auth/login", json={
        "email": "staff@test.com",
        "password": "staff123"
    })
    return response.json()["access_token"]