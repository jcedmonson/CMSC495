import pytest

from conftest import MOCK_USERS


async def test_get_connections_fail_not_found(pop_client, user_jwt_token):
    response = await pop_client.get("/connections/user/99999", headers=user_jwt_token)
    assert response.status_code == 404, response.text

async def test_get_connections_success_empty(pop_client):
    user = MOCK_USERS[0]
    response = await pop_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

async def test_add_connection_one(pop_client):
    current_user = MOCK_USERS[0]
    other_user = MOCK_USERS[1]

    # validate that the user had no connections
    response = await pop_client.get(f"/connections/user/{current_user.user_id}", headers=current_user.jwt_token)
    assert response.status_code == 200, (current_user, response.text)
    assert len(response.json()) == 0, (current_user, response.json())


    # Create a connection
    response = await pop_client.post(
        "/connections/user",
        json=other_user.to_json,
        headers=current_user.jwt_token
    )
    assert response.status_code == 201, other_user

    # Validate that the user now only has one connection
    response = await pop_client.get(f"/connections/user/{current_user.user_id}", headers=current_user.jwt_token)
    assert response.status_code == 200, (current_user, response.text)
    assert len(response.json()) == 1, (current_user, response.json())



@pytest.fixture(scope="module")
async def make_user_connections(pop_client):
    user_1 = MOCK_USERS[0]
    for user in MOCK_USERS[1:]:
        response = await pop_client.post(
            "/connections/user",
            json=user.to_json,
            headers=user_1.jwt_token
        )

    user_2 = MOCK_USERS[1]
    for user in MOCK_USERS[3:]:
        response = await pop_client.post(
            "/connections/user",
            json=user.to_json,
            headers=user_2.jwt_token
        )
        assert response.status_code == 201, (user, response.text)


async def test_connections_made(pop_client, make_user_connections):
    user = MOCK_USERS[0]
    response = await pop_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) == len(MOCK_USERS[1:])

    user = MOCK_USERS[1]
    response = await pop_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    assert len(response.json()) == len(MOCK_USERS[3:])

async def test_duplicate_connection(pop_client, make_user_connections):
    user = MOCK_USERS[0]
    response = await pop_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

    connections = response.json()
    assert len(connections) == len(MOCK_USERS[1:])

    response = await pop_client.post(
        "/connections/user",
        json={
            "user_id": connections[0].get("user_id"),
            "user_name": connections[0].get("user_name"),
            "first_name": connections[0].get("first_name"),
            "last_name": connections[0].get("last_name")
        },
        headers=user.jwt_token
    )
    assert response.status_code == 403, user





