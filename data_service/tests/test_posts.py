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


async def test_login_user_not_found(async_app_client):
    response = await async_app_client.get("/posts")

    assert response.status_code == 200, response.text
