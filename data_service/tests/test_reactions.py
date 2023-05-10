from httpx import AsyncClient

from conftest import MockUser, get_random_post, database

from endpoints import crud
import models.padentic_models as p_model


async def test_reaction(async_client: AsyncClient,
                        mock_users: list[MockUser]) -> None:
    post, user = await get_random_post(async_client, mock_users)

    reaction = p_model.PostReaction.parse_obj({"reaction": 3, **user.dict()})

    response = await async_client.post(
        f"/posts/{post.post_id}/reaction",
        json=reaction.dict(),
        headers=user.jwt_token)

    assert response.status_code == 201, (user, response.text)


async def test_duplicate_reaction(async_client: AsyncClient,
                                  mock_users: list[MockUser]) -> None:
    # Get random data
    post, user = await get_random_post(async_client, mock_users)

    # Create a reaction
    reaction = p_model.PostReaction.parse_obj({"reaction": 3, **user.dict()})

    # Add a reaction
    await async_client.post(
        f"/posts/{post.post_id}/reaction",
        json=reaction.dict(),
        headers=user.jwt_token)

    # Fetch the post to extract the reaction we just added
    response = await async_client.get(
        f"/posts/{post.post_id}",
        headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    posts = response.json()

    posted_reaction = {}
    for react in posts.get("reactions"):
        if react.get("user_id") == user.user_id:
            posted_reaction = react
    assert posted_reaction


    # React to the same post; this should update the reaction with the new data
    response = await async_client.post(
        f"/posts/{post.post_id}/reaction",
        json=reaction.dict(),
        headers=user.jwt_token)
    assert response.status_code == 201, (user, response.text)

    # Fetch the post again to compare the new timestamps
    response = await async_client.get(
        f"/posts/{post.post_id}",
        headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)
    posts = response.json()

    new_reaction = {}
    for react in posts.get("reactions"):
        if react.get("user_id") == user.user_id:
            new_reaction = react
    assert new_reaction


    assert posted_reaction.get("user_id") == new_reaction.get("user_id"), (
        new_reaction, posted_reaction)
    assert posted_reaction.get("reaction_date") != new_reaction.get(
        "reaction_date"), (new_reaction, posted_reaction)
