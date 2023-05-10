from random import choice

from httpx import AsyncClient

from models import padentic_models as p_model
from conftest import MockUser, get_random_post



async def test_post_comment(async_client: AsyncClient,
                            mock_users: list[MockUser]) -> None:
    post, user_chosen = await get_random_post(async_client, mock_users)
    post_count = len(post.comments)

    comment = p_model.PostCommentBody.parse_obj(
        { **post.dict(), "content": user_chosen.gen_comment()})

    response = await async_client.post(
        f"/posts/{post.post_id}/comment",
        json=comment.dict(),
        headers=user_chosen.jwt_token
    )
    assert response.status_code == 201, (response.text, post, user_chosen)

    response = await async_client.get(f"/posts/{post.post_id}",
                                      headers=user_chosen.jwt_token)
    assert response.status_code == 200, (user_chosen, response.text)
    assert len(response.json().get("comments")) > post_count

    comment = response.json().get("comments")[-1]

    response = await async_client.get(f"/posts/{post.post_id}/{comment.get('comment_id')}",
                                      headers=user_chosen.jwt_token)
    assert response.status_code == 200, (user_chosen, response.text)



async def test_fetch_missing_post(async_client: AsyncClient,
                                  mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get("/posts/999999999/9999999",
                                      headers=user.jwt_token)
    assert response.status_code == 404, (user, response.text)


async def test_fetch_missing_comment(async_client: AsyncClient,
                                     mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get("/posts/timeline/?limit=1",
                                      headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

    post_id = response.json()[0].get("post_id")
    response = await async_client.get(f"/posts/{post_id}/9999999",
                                      headers=user.jwt_token)
    assert response.status_code == 404, (user, response.text)



