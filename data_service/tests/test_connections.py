import pytest

from conftest import MOCK_USERS

# @pytest.fixture(scope="module")
# async def authed_user(pop_client, user_jwt_token):
#     """
#     Fixture does a request to fetch a user_id that is valid in the db table
#     """
#     response = await pop_client.get("/users", headers=user_jwt_token)
#     assert response.status_code == 200, response.text
#
#     current_user_json = response.json()[2]
#     other_user_json = response.json()[3]
#
#     assert current_user_json is not None
#     assert other_user_json is not None
#
#     current_user, other_user = None, None
#     for user in MOCK_USERS:
#         if user.user_name == current_user_json.get("user_name"):
#             current_user = user
#         elif user.user_name == other_user.get("user_name"):
#             other_user = user
#
#     assert current_user is not None
#     assert other_user is not None




async def test_get_connections_fail_not_found(pop_client, user_jwt_token):
    response = await pop_client.get("/connections/user/99999", headers=user_jwt_token)
    assert response.status_code == 404, response.text

async def test_get_connections_success_empty(pop_client):
    user = MOCK_USERS[0]
    response = await pop_client.get(f"/connections/user/{user.user_id}", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

async def test_add_connection(pop_client):
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
    assert response.json() == 1, (current_user, response.json())



