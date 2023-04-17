from httpx import AsyncClient
import pytest

from auth_app.main import auth_app

@pytest.fixture
async def async_app_client():
    async with AsyncClient(app=auth_app, base_url='http://127.0.0.1:8888') as client:
        yield client


async def test_create_user_invalid(async_app_client):
    response = await async_app_client.post(
        "/login",
        json={},
    )
    assert response.status_code == 422, response.text


async def test_create_user_valid(async_app_client):
    response = await async_app_client.post(
        "/login",
        json={
            "user_name": "sasquach",
            "password": "password"
        },
    )
    assert response.status_code == 404, response.text
