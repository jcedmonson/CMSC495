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
    other_user = choice(mock_users)

    # validate that the user had no connections
    response = await async_client.get(f"/connections/user/{current_user.user_id}", headers=current_user.jwt_token)
    assert response.status_code == 200, (current_user, response.text)
    assert len(response.json()) == 0, (current_user, response.json())


    # Create a connection
    response = await async_client.post(
        "/connections/user",
        json=other_user.to_json,
        headers=current_user.jwt_token
    )
    assert response.status_code == 201, other_user

    # Validate that the user now only has one connection
    response = await async_client.get(f"/connections/user/{current_user.user_id}", headers=current_user.jwt_token)
    assert response.status_code == 200, (current_user, response.text)
    assert len(response.json()) == 1, (current_user, response.json())

async def test_duplicate_connection(async_client: AsyncClient, 
                                    mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

    connected_with = choice(response.json())


    response = await async_client.post(
        "/connections/user",
        json={
            "user_id": connected_with.get("user_id"),
            "user_name": connected_with.get("user_name"),
            "first_name": connected_with.get("first_name"),
            "last_name": connected_with.get("last_name")
        },
        headers=user.jwt_token
    )
    assert response.status_code == 403, user






