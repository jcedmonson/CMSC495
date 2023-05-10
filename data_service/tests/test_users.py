from httpx import AsyncClient

from conftest import MockUser

async def test_get_all_users(async_client: AsyncClient,
                             default_user: MockUser,
                             mock_users: list[MockUser]) -> None:

    response = await async_client.get("/users", headers=default_user.jwt_token)
    assert response.status_code == 200, response.text


async def test_get_user_success(async_client: AsyncClient,
                                default_user: MockUser,
                                mock_users: list[MockUser]) -> None:
    response = await async_client.get(f"/users/{default_user.user_name}", headers=default_user.jwt_token)
    assert response.status_code == 200, response.text
    assert response.json()[0].get("user_name") == default_user.user_name, response.json()


async def test_get_user_fail(async_client: AsyncClient,
                             default_user: MockUser) -> None:
    response = await async_client.get("/users/tofu", headers=default_user.jwt_token)
    assert response.status_code == 404, response.text

async def test_get_user_like(async_client: AsyncClient,
                             default_user: MockUser) -> None:
    user = "j"
    response = await async_client.get(f"/users/{user}", headers=default_user.jwt_token)
    assert response.status_code == 200, response.text

    payload = response.json()
    assert len(payload) > 0, payload


