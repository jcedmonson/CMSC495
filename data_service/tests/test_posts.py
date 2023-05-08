from conftest import MOCK_USERS

async def test_empty_posts(pop_client):
    user = MOCK_USERS[0]
    response = await pop_client.get(f"/posts", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) == 0, (user, "\n", response.text, "\n", response.json())

async def test_post_too_large(pop_client):
    user = MOCK_USERS[0]
    response = await pop_client.post(f"/posts",
                                     json={"body": "hi" * 2048},
                                     headers=user.jwt_token)
    assert response.status_code == 400, (user, response.text)

async def test_post_too_small(pop_client):
    user = MOCK_USERS[0]
    response = await pop_client.post(f"/posts",
                                     json={"body": ""},
                                     headers=user.jwt_token)
    assert response.status_code == 400, (user, response.text)
