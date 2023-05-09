from random import choice

from httpx import AsyncClient

from conftest import MockUser

async def test_get_connections_fail_not_found(async_client: AsyncClient,
                                              mock_users: list[MockUser]) -> None:

    user = choice(mock_users)
    response = await async_client.get("/connections/user/99999", headers=user.jwt_token)
    assert response.status_code == 404, response.text

async def test_get_connections_success_empty(async_client: AsyncClient,
                                             mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

async def test_add_connection_one(async_client: AsyncClient,
                                  mock_users: list[MockUser]) -> None:
    current_user = choice(mock_users)

    # validate that the user had no connections
    response = await async_client.get(f"/connections/user/{current_user.user_id}", headers=current_user.jwt_token)
    assert response.status_code == 200, (current_user, response.text)
    connections = len(response.json())


    # Create a connection
    connection_made = False
    while not connection_made:
        other_user = choice(mock_users)
        response = await async_client.post(
            "/connections/user",
            json=other_user.to_json,
            headers=current_user.jwt_token
        )
        if response.status_code == 201:
            connection_made = True

    # Validate that the user now only has one connection
    response = await async_client.get(f"/connections/user/{current_user.user_id}", headers=current_user.jwt_token)
    assert response.status_code == 200, (current_user, response.text)
    assert connections < len(response.json())

async def test_duplicate_connection(async_client: AsyncClient,
                                    mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    connect_with = choice(mock_users)

    await async_client.post(
        "/connections/user",
        json=connect_with.to_json,
        headers=user.jwt_token
    )

    response = await async_client.post(
        "/connections/user",
        json=connect_with.to_json,
        headers=user.jwt_token
    )

    assert response.status_code == 403, user






