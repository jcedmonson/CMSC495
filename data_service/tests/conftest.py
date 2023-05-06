import asyncio
from dataclasses import dataclass

import pytest
from httpx import AsyncClient

from main import data_app, get_settings
from endpoints.database import database
from models.base import Base

@dataclass
class MockUser:
    user_name: str
    first_name: str
    last_name: str
    password: str
    email: str

MOCK_USERS = [
    MockUser("johncena", "john", "cena", "can't see my password", "invi@gmail.com"),
    MockUser("JackRogers", "Jack", "Rogers", "some password", "jack@gmail.com"),
    MockUser("hi", "ho", "cena", "pass", "pass@gmail.com"),
    MockUser("hoi", "ho", "cena", "pass", "p2ass@gmail.com"),
]

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
        "/auth/user",
        json={
            "user_name": username,
            "first_name": "johnson",
            "last_name": "also johnson",
            "password": password,
            "email": "johnson@johnson.com"
        },
    )
    assert response.status_code == 201

    # log in with that user
    response = await async_app_client.post(
        "/auth/login",
        json={
            "user_name": username,
            "password": password,
        },
    )
    assert response.status_code == 200

    # Verify the token with the /user endpoint
    headers = {"Authorization": f"Bearer {response.json().get('token')}"}
    response = await async_app_client.get("/auth/user", headers=headers)
    assert response.status_code == 200, response.text

    yield headers


@pytest.fixture(scope="module")
async def pop_client(async_app_client):
    for user in MOCK_USERS:
        response = await async_app_client.post(
            "/auth/user",
            json=user.__dict__
        )
        assert response.status_code == 201, response.text


    yield async_app_client