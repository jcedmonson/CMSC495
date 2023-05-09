import asyncio
from dataclasses import dataclass
from random import choice

import pytest
from httpx import AsyncClient
from faker import Faker

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
    user_id: int | None = None
    jwt_token: dict | None = None

    @property
    def user_creation_json(self) -> dict:
        return {
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "email": self.email
        }

    @property
    def to_json(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    @property
    def comment(self) -> str:
        fake = Faker()
        return fake.text()[0:1000]


def make_mock_user(count: int) -> list[MockUser]:
    fake = Faker()
    users = []
    for i in range(0, count):
        users.append(MockUser(
            fake.user_name(),
            fake.first_name(),
            fake.last_name(),
            fake.password(),
            fake.email()
        ))
    return users


MOCK_USERS = [
    MockUser("johncena", "john", "cena", "can't see my password",
             "invi@gmail.com"),
    MockUser("JackRogers", "Jack", "Rogers", "some password",
             "jack@gmail.com"),
]
MOCK_USERS.extend(make_mock_user(20))


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


@pytest.fixture(scope="session")
async def async_client(event_loop):
    # async with AsyncClient(app=data_app,
    #                        base_url="http://127.0.0.1:8080") as client:
    async with AsyncClient(base_url="http://127.0.0.1:8080") as client:

        await data_app.router.startup()

        yield client

        # Drop tables during tear down
        async with database.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await data_app.router.shutdown()


@pytest.fixture(scope="session")
async def user_jwt_token(async_client):
    username = "sasquach22"
    password = "johnson"
    # Create user
    response = await async_client.post(
        "/auth/user",
        json={
            "user_name": username,
            "first_name": "johnson",
            "last_name": "also johnson",
            "password": password,
            "email": "johnson@johnson.com"
        },
    )
    # log in with that user
    response = await async_client.post(
        "/auth/login",
        json={
            "user_name": username,
            "password": password,
        },
    )
    assert response.status_code == 200

    # Verify the token with the /user endpoint
    headers = {"Authorization": f"Bearer {response.json().get('token')}"}
    response = await async_client.get("/auth/user", headers=headers)
    assert response.status_code == 200, response.text

    yield headers


@pytest.fixture(scope="session")
async def populate_users(async_client):
    for user in MOCK_USERS:
        # Create the user
        response = await async_client.post(
            "/auth/user",
            json=user.user_creation_json
        )
        assert response.status_code == 201, response.text

        # Authenticate user to extract the jwt token
        response = await async_client.post(
            "/auth/login",
            json={
                "user_name": user.user_name,
                "password": user.password,
            },
        )
        assert response.status_code == 200

        # save the jwt token into the object
        user.jwt_token = {
            "Authorization": f"Bearer {response.json().get('token')}"}
        user.user_id = response.json().get("user_id")

        # Authenticate with it to ensure that it works
        response = await async_client.get("/auth/user", headers=user.jwt_token)
        assert response.status_code == 200, response.text


@pytest.fixture(scope="session")
async def populate_connections(async_client, populate_users):
    for _ in range(0, 100):
        user = choice(MOCK_USERS)
        follow = choice(MOCK_USERS)

        response = await async_client.post(
            "/connections/user",
            json=follow.to_json,
            headers=user.jwt_token
        )

        if response.status_code == 403:
            if response.text == "Connection between users already exists":
                continue
        else:
            assert response.status_code == 201, (user, follow, response.text)


@pytest.fixture(scope="session")
async def populate_posts(async_client, populate_connections):
    for _ in range(0, 100):
        user = choice(MOCK_USERS)

        response = await async_client.post(
            "/posts",
            json={"content": user.comment},
            headers=user.jwt_token
        )

        assert response.status_code == 201, (user, response.text)

@pytest.fixture(scope="function")
async def user():
    yield choice(MOCK_USERS)
