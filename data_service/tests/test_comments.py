from random import choice

from httpx import AsyncClient

from models import padentic_models as p_model
from conftest import MockUser

async def test_post_comment(async_client: AsyncClient, mock_users: list[MockUser]) -> None:
    post: p_model.UserPost | None = None
    user_chosen: MockUser | None = None

    while post is None:
        other_user = choice(mock_users)
        response = await async_client.get("/posts", headers=other_user.jwt_token)
        assert response.status_code == 200, (other_user, response.text)
        posts = response.json()
        if posts:
            post = p_model.UserPost.parse_obj(choice(posts))
            user_chosen = other_user

    post_count = len(post.comments)
    comment = p_model.PostCommentBody.parse_obj({"content": user_chosen.comment, **post.dict()})


    response = await async_client.post(
        f"/posts/{post.post_id}/comment",
        json=comment.dict(),
        headers=user_chosen.jwt_token
    )
    assert response.status_code == 201, (response.text, post, user_chosen)

    response = await async_client.get(f"/posts/{post.post_id}", headers=user_chosen.jwt_token)
    assert response.status_code == 200, (user_chosen, response.text)
    assert len(response.json().get("comments")) > post_count

async def test_fetch_missing_post(async_client: AsyncClient,
                                     mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get("/posts/999999999/9999999", headers=user.jwt_token)
    assert response.status_code == 404, (user, response.text)

async def test_fetch_missing_comment(async_client: AsyncClient,
                                  mock_users: list[MockUser]) -> None:
    user = choice(mock_users)
    response = await async_client.get("/posts/timeline/?limit=1", headers=user.jwt_token)
    assert response.status_code == 200, (user, response.text)

    post_id = response.json()[0].get("post_id")
    response = await async_client.get(f"/posts/{post_id}/9999999", headers=user.jwt_token)
    assert response.status_code == 404, (user, response.text)



