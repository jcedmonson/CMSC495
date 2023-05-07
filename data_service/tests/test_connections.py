from conftest import MOCK_USERS

async def test_get_connections_fail_not_found(pop_client, user_jwt_token):
    response = await pop_client.get("/connections/user/99999", headers=user_jwt_token)
    assert response.status_code == 404, response.text

async def test_get_connections_success_empty(pop_client, user_jwt_token):
    response = await pop_client.get("/users", headers=user_jwt_token)
    assert response.status_code == 200, response.text

    user_id = response.json()[2].get("user_id")
    assert user_id is not None

    response = await pop_client.get(f"/connections/user/{user_id}", headers=user_jwt_token)
    assert response.status_code == 200, (user_id, response.text)

