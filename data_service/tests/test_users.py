async def test_get_all_users(pop_client, user_jwt_token):
    response = await pop_client.get("/users", headers=user_jwt_token)
    assert response.status_code == 200, response.text

async def test_get_user_success(pop_client, user_jwt_token):
    user = "johncena"
    response = await pop_client.get(f"/users/{user}", headers=user_jwt_token)
    assert response.status_code == 200, response.text
    assert response.json()[0].get("user_name") == user, response.json()

async def test_get_user_fail(async_app_client, user_jwt_token):
    response = await async_app_client.get("/users/tofu", headers=user_jwt_token)
    assert response.status_code == 404, response.text

async def test_get_user_like(pop_client, user_jwt_token):
    user = "j"
    response = await pop_client.get(f"/users/{user}", headers=user_jwt_token)
    assert response.status_code == 200, response.text

    payload = response.json()
    assert len(payload) > 1, payload


