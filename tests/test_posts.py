import pytest
from typing import List
from app import schemas
from tests.conftest import create_test_posts

def test_get_all_posts(authorized_client, create_test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostVoteOut(**post)

    posts = list(map(validate, res.json()))

    assert len(res.json()) == len(create_test_posts)
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_posts(client, create_test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_posts(client, create_test_posts):
    res = client.get(f"/posts/{create_test_posts[0].id}")
    assert res.status_code == 401
    
def test_get_one_post_not_exist(authorized_client, create_test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404
    
def test_get_one_post(authorized_client, create_test_posts):
    res = authorized_client.get(f"/posts/{create_test_posts[0].id}")
    post = schemas.PostVoteOut(**res.json())
    assert post.Post.id == create_test_posts[0].id
    assert post.Post.content == create_test_posts[0].content
    assert post.Post.title == create_test_posts[0].title
    
@pytest.mark.parametrize("title, content, published",[
    ("summer", "summer content", True),
    ("winter", "winter content", False),
    ("spring", "spring content", False),
    ("autumn", "autumn content", True)
    ])
def test_create_post(authorized_client, test_user, title, content, published, create_test_posts):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.PostOut(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.user_id == test_user["id"]
    
def test_create_default_published_true(authorized_client, test_user, create_test_posts):
    res = authorized_client.post("/posts/", json={"title": "title", "content": "content"})
    post = schemas.PostOut(**res.json())
    assert res.status_code == 201
    assert post.title == "title"
    assert post.content == "content"
    assert post.published == True
    assert post.user_id == test_user["id"]


def test_unauthorized_user_create_posts(client, create_test_posts):
    res = client.post("/posts/", json={"title": "title", "content": "content"})
    assert res.status_code == 401  
    
def test_unauthorized_user_delete_posts(client, create_test_posts):
    res = client.delete(f"/posts/{create_test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, create_test_posts):
    res = authorized_client.delete(f"/posts/{create_test_posts[0].id}")
    assert res.status_code == 204
    

def test_delete_post_non_exist(authorized_client, test_user, create_test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, create_test_posts):
    res = authorized_client.delete(
        f"/posts/{create_test_posts[3].id}")
    assert res.status_code == 204


def test_update_post(authorized_client, test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": create_test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{create_test_posts[0].id}", json=data)
    updated_post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": create_test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{create_test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, create_test_posts):
    res = client.put(
        f"/posts/{create_test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": create_test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404