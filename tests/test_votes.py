import pytest

from app import models


@pytest.fixture()
def test_vote(create_test_posts, session, test_user):
    new_vote = models.Vote(post_id=create_test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, create_test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": create_test_posts[3].id, "sign": 1}
    )
    print(res.status_code)
    print(res.json())
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, create_test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": create_test_posts[3].id, "sign": 1}
    )
    assert res.status_code == 409


def test_delete_vote(authorized_client, create_test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": create_test_posts[3].id, "sign": 0}
    )
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, create_test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": create_test_posts[3].id, "sign": 0}
    )
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, create_test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 80000, "sign": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, create_test_posts):
    res = client.post("/vote/", json={"post_id": create_test_posts[3].id, "sign": 1})
    assert res.status_code == 401
