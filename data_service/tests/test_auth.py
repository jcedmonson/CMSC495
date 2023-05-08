from httpx import AsyncClient

from endpoints.database import database
from models.base import Base


async def test_login_user_not_found(async_app_client):
    response = await async_app_client.post(
        "/auth/login",
        json={
            "user_name": "sasquach",
            "password": "password"
        },
    )
    assert response.status_code == 401, response.text


async def test_login_user_invalid_req(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/auth/login",
        json={
            "user_name": "sasquach"
        },
    )
    assert response.status_code == 422, response.text


async def test_user_invalid_req(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/auth/user",
        json={
            "user_name": "sasquach"
        },
    )
    assert response.status_code == 422, response.text


async def test_user_valid_creation(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/auth/user",
        json={
            "user_name": "sasquach",
            "first_name": "johnson",
            "last_name": "also johnson",
            "password": "password",
            "email": "johnson@johnson.com"
        },
    )
    assert response.status_code == 201, response.text



async def test_user_valid_token(async_app_client: AsyncClient) -> None:
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    username = "sasquach22"
    password = "johnson"
    # Create user
    response = await async_app_client.post(
        "/auth/user",
        json={
            "user_name": username,
            "first_name": "johnson",
            "last_name": "also johnson",
            "password": password,
            "email": "johnson@johnson.com"
        },
    )
    assert response.status_code == 201, response.text

    # log in with that user
    response = await async_app_client.post(
        "/auth/login",
        json={
            "user_name": username,
            "password": password,
        },
    )
    assert response.status_code == 200, response.text

    # Verify the token with the /user endpoint
    headers = {"Authorization": f"Bearer {response.json().get('token')}"}
    response = await async_app_client.get("/auth/user", headers=headers)
    assert response.status_code == 200, response.text