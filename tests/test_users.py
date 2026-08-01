import pytest
from fastapi import status
from app import schemas
from app.config import settings
import jwt


# @pytest.fixture
# def test_user(client):
#     user_data = {"email": "fun@gmail.com", "password": "passworddd"}
#     res = client.post("/users/", json=user_data)
#     new_user = res.json()
#     new_user["password"] = user_data["password"]
#     assert res.status_code == 201
#     return new_user


# def test_root(client):
#     res = client.get("/")
#     # print(res.json().get('message'))
#     assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "passworddd"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_duplicate_user(client, test_user):
    #нужно указывать /users/, потому что в отличии от fastapi, pytest не понимает что /users нужно перекинуть на /users/ (так как в user.py мы используем префикс /users а после в endpoint мы добавляем "/")
    client.post("/users/", json={"email": "hello123@gmail.com", "password": "passworddd"})
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "passworddd"})
    
    assert res.json()["detail"] == "Email already registered"
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code", [
    (None, "password123", 422),
    ("fun@gmail.com", "wrongpassword", 403),
    ("wrongemail", "passworddd", 403),
    ("wrongemail", "wrongpassword", 403),
    ("fun@gmail.com", None, 422) 
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
        