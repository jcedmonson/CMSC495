from random import choice

from httpx import AsyncClient

from conftest import MockUser

async def test_post_too_large(async_client: AsyncClient,
                              mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.post(f"/posts",
                                         json={"content": "hi" * 2048},
                                         headers=user.jwt_token)
    assert response.status_code == 400, (user, response.text)

async def test_post_too_small(async_client: AsyncClient,
                              mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.post(f"/posts",
                                         json={"content": ""},
                                         headers=user.jwt_token)
    assert response.status_code == 400, (user, response.text)

async def test_valid_post(async_client: AsyncClient,
                          mock_users: list[MockUser]) -> None:
    user = choice(mock_users)

    # Test that the user has no posts
    response = await async_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    post_count = len(response.json())

    # Create a post
    response = await async_client.post(f"/posts",
                                         json={"content": "This is a post"},
                                         headers=user.jwt_token)
    assert response.status_code == 201, (user, response.text)

    # Validate that a post was made
    response = await async_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert post_count < len(response.json())

async def test_post_retrival(async_client: AsyncClient,
                             mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get("/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)


async def test_get_all_posts(async_client: AsyncClient,
                             mock_users: list[MockUser]) -> None:
    user = choice(mock_users)

    response = await async_client.get("/posts/timeline/", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) <= 50

    response = await async_client.get("/posts/timeline/?limit=10", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) <= 10

    response = await async_client.get("/posts/timeline/?offset=10&limit=10", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) <= 10

async def test_get_post_by_id(async_client: AsyncClient,
                              mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get("/posts/0", headers=user.jwt_token)
    assert response.status_code == 404, (user, response.text)

    response = await async_client.get("/posts/1", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

    response = await async_client.get("/posts/2", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

    response = await async_client.get("/posts/5", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)


async def test_post_removal(async_client: AsyncClient,
                            mock_users: list[MockUser]) -> None:

    user = choice(mock_users)

    # Create a post
    msg = user.gen_comment()
    response = await async_client.post(f"/posts",
                                       json={"content": msg},
                                       headers=user.jwt_token)
    assert response.status_code == 201, (user, response.text)

    # Validate that a post was made
    response = await async_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    posts = response.json()

    posted_msg = None
    for post in posts:
        if post.get("content") == msg:
            posted_msg = post
            break

    assert posted_msg is not None

    post_id = posted_msg.get("post_id")
    assert isinstance(post_id, int)
    response = await async_client.post(f"/posts/delete",
                                      json={"post_id": post_id},
                                      headers=user.jwt_token)
    assert response.status_code == 201, (user, response.text)

    # confirm that it was removed
    response = await async_client.get(f"/posts/{posted_msg.get('post_id')}", headers=user.jwt_token)
    assert response.status_code == 404, (user, response.text)

