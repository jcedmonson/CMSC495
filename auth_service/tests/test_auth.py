import asyncio

import pytest
from httpx import AsyncClient

from auth_app.main import auth_app

@pytest.fixture(scope="session")
def event_loop():
    """
    There is a bug with scope=module, async pytest, and event loops. To fix
    it you must declare an event loop as "session" and use that accross
    all the async pytest functions
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def async_app_client(event_loop):
    async with AsyncClient(app=auth_app, base_url='http://127.0.0.1:8888') as client:
        await auth_app.router.startup()
        yield client
        await auth_app.router.shutdown()


async def test_login_user_not_found(async_app_client):
    response = await async_app_client.post(
        "/login",
        json={
            "user_name": "sasquach",
            "password": "password"
        },
    )
    assert response.status_code == 404, response.text

async def test_create_user_valid(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/login",
        json={
            "user_name": "sasquach",
            "password": "password"
        },
    )
    assert response.status_code == 401, response.text

