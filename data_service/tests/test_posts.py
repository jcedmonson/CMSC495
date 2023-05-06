# async def test_missing_authorization_token(async_app_client):
#     response = await async_app_client.get("/posts")
#     assert response.status_code == 422, response.text
#
# async def test_post_endpoint(async_app_client, user_jwt_token):
#     response = await async_app_client.get("/posts", headers=user_jwt_token)
#     assert response.status_code == 200, response.text
