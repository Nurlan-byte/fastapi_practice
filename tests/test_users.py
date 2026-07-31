
from fastapi.testclient import TestClient
import pytest
from fastapi import status
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.database import get_db, Base
from alembic import command 


engine = create_engine("postgresql://postgres:password123@localhost:5432/fastapi_test")

TestingSessionLocal = sessionmaker(engine, autoflush=False)



# class Base(DeclarativeBase):
#     pass


# def overrides_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = overrides_get_db





@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def overrides_get_db():
        try:
            yield session
        finally:
            session.close()
    
    
    app.dependency_overrides[get_db] = overrides_get_db
    #run our code before we run our test
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    #run our code after our test finishes

def test_root(client):
    res = client.get("/")
    # print(res.json().get('message'))
    assert res.json().get('message') == "Hello World"
    assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "passworddd"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_duplicate_user(client):
    client.post("/users/", json={"email": "hello123@gmail.com", "password": "passworddd"})
    
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "passworddd"})
    
    assert res.json()["detail"] == "Email already registered"
    assert res.status_code == status.HTTP_400_BAD_REQUEST
