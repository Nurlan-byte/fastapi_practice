
from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import pytest
from .database import client, session




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





@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
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

@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "fun@gmail.com", "password": "passworddd"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert res.status_code == 201
    return new_user
    #run our code after our test finishes
    
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}" 
    }
    
    return client


@pytest.fixture
def create_test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    posts = list(map(create_post_model, posts_data))

    session.add_all(posts)
    session.commit()
    # session.refresh()
    posts = session.query(models.Post).all()
    return posts