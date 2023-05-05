import asyncio

import pytest
from httpx import AsyncClient

from data_app.main import data_app, get_settings
from data_app.backend.database import database
from models.base import Base


@pytest.fixture(scope="session")
def event_loop():
    """
    There is a bug with scope=module, async pytest, and event loops. To fix
    it you must declare an event loop as "session" and use that accross
    all the async pytest functions
    """
    get_settings().drop_tables = True
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def async_app_client(event_loop):
    async with AsyncClient(app=data_app,
                           base_url="http://127.0.0.1:8080") as client:
        async with database.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await data_app.router.startup()
        yield client
        await data_app.router.shutdown()


@pytest.fixture(scope="module")
async def user_jwt_token(event_loop):
    async with AsyncClient(base_url="http://auth_service:8888") as client:

        username = "sasquach22"
        password = "johnson"
        # Create user
        response = await client.post(
            "/user",
            json={
                "user_name": username,
                "first_name": "johnson",
                "last_name": "also johnson",
                "password": password,
                "email": "johnson@johnson.com"
            },
        )
        # log in with that user
        response = await client.post(
            "/login",
            json={
                "user_name": username,
                "password": password,
            },
        )
        # Verify the token with the /user endpoint
        headers = {"Authorization": f"Bearer {response.json().get('token')}"}
        response = await client.get("/user", headers=headers)
        assert response.status_code == 200, response.text

    yield headers


async def test_missing_authorization_token(async_app_client):
    response = await async_app_client.get("/posts")
    assert response.status_code == 422, response.text

async def test_post_endpoint(async_app_client, user_jwt_token):
    response = await async_app_client.get("/posts", headers=user_jwt_token)
    assert response.status_code == 200, response.text

async def test_users_endpoint(async_app_client, user_jwt_token):
    response = await async_app_client.get("/users", headers=user_jwt_token)
    assert response.status_code == 200, response.text
