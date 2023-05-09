import asyncio
from random import choice

import pytest
from httpx import AsyncClient
from faker import Faker
from pydantic import BaseModel, EmailStr

from main import data_app, get_settings
from endpoints.database import database
from endpoints import crud
from models import padentic_models as p_model
from models.base import Base

PRODUCE_COUNT = 5
FAKE = Faker()


class MockUser(BaseModel):
    class Config:
        orm_mode = True

    user_name: str
    first_name: str
    last_name: str
    password: str
    email: EmailStr
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

    @staticmethod
    def gen_comment() -> str:
        return FAKE.text()[0:1000]


def make_mock_user(count: int) -> list[MockUser]:
    users = []
    for i in range(0, count):
        users.append(MockUser(
            user_name=FAKE.user_name(),
            first_name=FAKE.first_name(),
            last_name=FAKE.last_name(),
            password="password",
            email=FAKE.email()
        ))
    return users


@pytest.fixture(scope="session")
def event_loop():
    """
    There is a bug with scope=module, async pytest, and event loops. To fix
    it you must declare an event loop as "session" and use that accross
    all the async pytest functions
    """
    get_settings().drop_tables = False
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop

    loop.close()


@pytest.fixture(scope="session")
async def async_client(event_loop) -> AsyncClient:
    async with AsyncClient(app=data_app,
                           base_url="http://127.0.0.1:8080") as client:
        # async with AsyncClient(base_url="http://127.0.0.1:8080") as client:

        await data_app.router.startup()

        # Drop tables during tear down
        if get_settings().drop_tables:
            async with database.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)


        yield client

        await data_app.router.shutdown()


@pytest.fixture(scope="session")
async def default_user(async_client) -> MockUser:
    user = MockUser(
        user_name="john_cena",
        first_name="john",
        last_name="cena",
        password="password",
        email="john@cena.com")

    # Create the default user (might fail if they exist, its k)
    await async_client.post(
        "/auth/user",
        json=user.user_creation_json,
    )

    # log in with that user
    response = await async_client.post(
        "/auth/login",
        json={
            "user_name": user.user_name,
            "password": user.password,
        },
    )
    assert response.status_code == 200
    # Verify the token with the /user endpoint
    # save the jwt token into the object
    user.jwt_token = {
        "Authorization": f"Bearer {response.json().get('token')}"}
    user.user_id = response.json().get("user_id")

    yield user


@pytest.fixture(scope="session")
async def create_users(async_client: AsyncClient, default_user: MockUser) -> \
        tuple[list[MockUser], bool]:
    # Fetch all users to see if we need to generate them
    response = await async_client.get("/users", headers=default_user.jwt_token)
    assert response.status_code == 200, response.text
    users = response.json()

    new_users = False
    if len(users) < PRODUCE_COUNT:
        new_users = True
        create_count = PRODUCE_COUNT - len(users)
        users = make_mock_user(create_count)
        for user in users:
            # Create the user
            response = await async_client.post(
                "/auth/user",
                json=user.user_creation_json
            )
            assert response.status_code == 201, response.text

    async with database.session() as session:
        users = await crud.get_all_users(session)
        mock_users: list[MockUser] = [
            MockUser.parse_obj({"password": "password", **i.__dict__}) for i in
            users]

    yield mock_users, new_users


@pytest.fixture(scope="session")
async def populated_users(async_client, create_users) -> tuple[
    list[MockUser], bool]:
    create_users, new_users = create_users

    for user in create_users:
        # Authenticate user to extract the jwt token
        response = await async_client.post(
            "/auth/login",
            json={
                "user_name": user.user_name,
                "password": user.password,
            },
        )
        assert response.status_code == 200, (user, response.text)

        # save the jwt token into the object
        user.jwt_token = {
            "Authorization": f"Bearer {response.json().get('token')}"}
        user.user_id = response.json().get("user_id")

        # Authenticate with it to ensure that it works
        response = await async_client.get("/auth/user", headers=user.jwt_token)
        assert response.status_code == 200, response.text

    yield create_users, new_users


async def populate_connections(async_client: AsyncClient,
                               mock_users: list[MockUser]) -> None:
    for _ in range(0, PRODUCE_COUNT):
        user = choice(mock_users)
        follow = choice(mock_users)

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


async def populate_posts(async_client: AsyncClient,
                         mock_users: list[MockUser]) -> None:
    for _ in range(0, PRODUCE_COUNT):
        user = choice(mock_users)

        response = await async_client.post(
            "/posts",
            json={"content": user.gen_comment()},
            headers=user.jwt_token
        )

        assert response.status_code == 201, (user, response.text)


async def populate_comments(async_client: AsyncClient,
                            mock_users: list[MockUser]) -> None:
    for _ in range(0, PRODUCE_COUNT):
        post, user = await get_random_post(async_client, mock_users)

        comment = p_model.PostCommentBody.parse_obj(
            {**post.dict(), "content": user.gen_comment()})

        response = await async_client.post(
            f"/posts/{post.post_id}/comment",
            json=comment.dict(),
            headers=user.jwt_token
        )
        assert response.status_code == 201, (response.text, post, user)


async def populate_reactions(async_client: AsyncClient,
                             mock_users: list[MockUser]) -> None:
    for _ in range(0, PRODUCE_COUNT):
        post, user = await get_random_post(async_client, mock_users)

        reaction = p_model.PostReaction.parse_obj({"reaction": 3, **user.dict()})

        response = await async_client.post(
            f"/posts/{post.post_id}/reaction",
            json=reaction.dict(),
            headers=user.jwt_token)

        assert response.status_code == 201, (user, response.text)


@pytest.fixture(scope="module")
async def mock_users(async_client, populated_users) -> list[MockUser]:
    mock_users, new_users = populated_users

    if new_users:
        await populate_connections(async_client, mock_users)
        await populate_posts(async_client, mock_users)
        await populate_comments(async_client, mock_users)
        await populate_reactions(async_client, mock_users)

    yield mock_users


async def get_random_post(async_client: AsyncClient,
                          mock_users: list[MockUser]) -> tuple[
    p_model.UserPost, MockUser]:
    post: p_model.UserPost | None = None
    user_chosen: MockUser | None = None

    while post is None:
        other_user = choice(mock_users)
        response = await async_client.get("/posts",
                                          headers=other_user.jwt_token)
        assert response.status_code == 200, (other_user, response.text)
        posts = response.json()

        if posts:
            post = p_model.UserPost.parse_obj(choice(posts))
            user_chosen = other_user

    return post, user_chosen
