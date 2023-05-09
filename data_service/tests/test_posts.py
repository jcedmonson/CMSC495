from random import choice

from models import padentic_models as p_model
from conftest import MOCK_USERS, MockUser

async def test_empty_posts(user: MockUser, async_client, populate_users):
    response = await async_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) == 0, (user, "\n", response.text, "\n", response.json())

async def test_post_too_large(user: MockUser, async_client, populate_users):
    response = await async_client.post(f"/posts",
                                         json={"content": "hi" * 2048},
                                         headers=user.jwt_token)
    assert response.status_code == 400, (user, response.text)

async def test_post_too_small(user: MockUser, async_client, populate_users):
    response = await async_client.post(f"/posts",
                                         json={"content": ""},
                                         headers=user.jwt_token)
    assert response.status_code == 400, (user, response.text)

async def test_valid_post(user: MockUser, async_client, populate_users):
    # Test that the user has no posts
    response = await async_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) == 0, (user, "\n", response.text, "\n", response.json())

    # Create a post
    response = await async_client.post(f"/posts",
                                         json={"content": "This is a post"},
                                         headers=user.jwt_token)
    assert response.status_code == 201, (user, response.text)

    # Validate that a post was made
    response = await async_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) == 1, (user, "\n", response.text, "\n", response.json())

async def test_post_retrival(user: MockUser, async_client, populate_posts):
    response = await async_client.get("/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) > 1, (user, "\n", response.text, "\n", response.json())


async def test_get_all_posts(user: MockUser, async_client, populate_posts):
    response = await async_client.get("/posts/timeline/", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) <= 50

    response = await async_client.get("/posts/timeline/?limit=10", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) <= 10

    response = await async_client.get("/posts/timeline/?offset=10&limit=10", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) <= 10

async def test_get_post_by_id(user: MockUser, async_client, populate_posts):
    response = await async_client.get("/posts/3", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

# async def test_post_comment(user: MockUser, async_client, populate_posts):
#     post: p_model.UserPost | None = None
#
#     while post is None:
#         other_user = choice(MOCK_USERS)
#         response = await async_client.get("/posts", headers=other_user.jwt_token)
#         assert response.status_code == 200, (user, response.text)
#         posts = response.json()
#         if posts:
#             post = p_model.UserPost.parse_obj(choice(posts))
#
#     comment = p_model.PostComment.parse_obj({"content": user.comment, **post.dict()})
#
#     import ipdb;ipdb.set_trace()
#
#     response = await async_client.post(
#         f"/posts/{post.post_id}/comment",
#         json=comment.dict(),
#         headers=user.jwt_token
#     )
#
#     assert response.status_code == 201, (response.text, post, user)
