from httpx import AsyncClient

from conftest import MockUser

async def test_login_user_not_found(async_client: AsyncClient, mock_users):
    response = await async_client.post(
        "/auth/login",
        json={
            "user_name": "sasquach33333",
            "password": "password"
        },
    )
    assert response.status_code == 401, response.text


async def test_login_user_invalid_req(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        json={
            "user_name": "sasquach"
        },
    )
    assert response.status_code == 422, response.text


async def test_user_invalid_req(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/user",
        json={
            "user_name": "sasquach"
        },
    )
    assert response.status_code == 422, response.text


# async def test_user_valid_creation(async_client: AsyncClient) -> None:
#     response = await async_client.post(
#         "/auth/user",
#         json={
#             "user_name": "sasquach",
#             "first_name": "johnson",
#             "last_name": "also johnson",
#             "password": "password",
#             "email": "johnson@johnson.com"
#         },
#     )
#     assert response.status_code == 201, response.text


async def test_user_valid_token(async_client: AsyncClient,
                                default_user: MockUser) -> None:
    # log in with that user
    response = await async_client.post(
        "/auth/login",
        json={
            "user_name": default_user.user_name,
            "password": default_user.password,
        },
    )
    assert response.status_code == 200, response.text

    # Verify the token with the /user endpoint
    headers = {"Authorization": f"Bearer {response.json().get('token')}"}
    response = await async_client.get("/auth/user", headers=headers)
    assert response.status_code == 200, response.text