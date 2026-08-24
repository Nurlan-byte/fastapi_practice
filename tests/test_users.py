import jwt
import pytest
from fastapi import status

from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "passworddd"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_duplicate_user(client, test_user):
    client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "passworddd"}
    )
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "passworddd"}
    )

    assert res.json()["detail"] == "Email already registered"
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        (None, "password123", 422),
        ("fun@gmail.com", "wrongpassword", 403),
        ("wrongemail", "passworddd", 403),
        ("wrongemail", "wrongpassword", 403),
        ("fun@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
