async def test_get_users(async_app_client, user_jwt_token):
    response = await async_app_client.get("/users", headers=user_jwt_token)
    assert response.status_code == 200, response.text



