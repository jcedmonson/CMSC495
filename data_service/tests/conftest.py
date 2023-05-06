import asyncio

import pytest
from httpx import AsyncClient

from main import data_app, get_settings
from endpoints.database import database
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
async def user_jwt_token(async_app_client):
    username = "sasquach22"
    password = "johnson"
    # Create user
    response = await async_app_client.post(
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
    response = await async_app_client.post(
        "/login",
        json={
            "user_name": username,
            "password": password,
        },
    )
    # Verify the token with the /user endpoint
    headers = {"Authorization": f"Bearer {response.json().get('token')}"}
    response = await async_app_client.get("/user", headers=headers)
    assert response.status_code == 200, response.text

    yield headers
