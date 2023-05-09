from httpx import AsyncClient

from conftest import MockUser, get_random_post

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
