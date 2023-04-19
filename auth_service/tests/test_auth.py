import asyncio

import pytest
from httpx import AsyncClient

from auth_app.main import auth_app, get_settings

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

async def test_login_user_invalid_req(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/login",
        json={
            "user_name": "sasquach"
        },
    )
    assert response.status_code == 422, response.text

async def test_user_invalid_req(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/user",
        json={
            "user_name": "sasquach"
        },
    )
    assert response.status_code == 422, response.text

async def test_user_valid_creation(async_app_client: AsyncClient) -> None:
    response = await async_app_client.post(
        "/user",
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
    response = await async_app_client.post(
        "/user",
        json={
            "user_name": "sasquach",
            "first_name": "johnson",
            "last_name": "also johnson",
            "password": "password",
            "email": "johnson@johnson.com"
        },
    )
    assert response.status_code == 201, response.text

    headers = {"Authorization": f"Bearer {response.json().get('token')}"}
    response = await async_app_client.get("/user2", headers=headers)

    import ipdb; ipdb.set_trace()

