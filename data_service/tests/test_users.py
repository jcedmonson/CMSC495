async def test_get_users(async_app_client, user_jwt_token):
    response = await async_app_client.get("/users", headers=user_jwt_token)
    assert response.status_code == 200, response.text

async def test_get_user(async_app_client, user_jwt_token):
    user = "sasquach22"
    response = await async_app_client.get(f"/users/{user}", headers=user_jwt_token)
    assert response.status_code == 200, response.text
    assert response.json().get("user_name") == user, response.json().get(user)

async def test_get_user_fail(async_app_client, user_jwt_token):
    response = await async_app_client.get(f"/users/fofu", headers=user_jwt_token)
    assert response.status_code == 404, response.text


