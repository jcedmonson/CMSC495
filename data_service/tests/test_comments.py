from random import choice

from models import padentic_models as p_model

from conftest import MOCK_USERS, MockUser

# async def test_post_comment(user: MockUser, async_client, populate_posts):
#     post: p_model.UserPost | None = None
#     user_chosen: MockUser | None = None
#
#     while post is None:
#         other_user = choice(MOCK_USERS)
#         response = await async_client.get("/posts", headers=other_user.jwt_token)
#         assert response.status_code == 200, (user, response.text)
#         posts = response.json()
#         if posts:
#             post = p_model.UserPost.parse_obj(choice(posts))
#             user_chosen = other_user
#
#     assert len(post.comments) == 0, post
#     comment = p_model.PostComment.parse_obj({"content": user.comment, **post.dict()})
#
#
#     response = await async_client.post(
#         f"/posts/{post.post_id}/comment",
#         json=comment.dict(),
#         headers=user.jwt_token
#     )
#     assert response.status_code == 201, (response.text, post, user)
#
#     response = await async_client.get(f"/posts/{post.post_id}", headers=user_chosen.jwt_token)
#     assert response.status_code == 200, (user, response.text)
#     assert len(post.comments) == 1, post
