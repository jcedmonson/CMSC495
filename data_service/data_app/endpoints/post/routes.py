import logging

from fastapi import APIRouter, Header, status, HTTPException

from models import padentic_models as p_model
import dependency_injection as inj
from endpoints.auth.jwt_token_handler import CurrentUser_t
from endpoints import crud

log = logging.getLogger("endpoints.posts")
post_routes = APIRouter(prefix="/posts")


@post_routes.get("", summary="Fetch all posts made by current user")
async def get_posts(current_user: CurrentUser_t,
                    session: inj.Session_t
                    ) -> list[p_model.UserPost]:
    log.debug(f"Querying posts for {current_user.user_name}")
    result = await crud.get_posts(session, current_user)
    return result


@post_routes.post("", status_code=201, summary="Submit a post")
async def set_post(post: p_model.UserPostBody,
                   current_user: CurrentUser_t,
                   session: inj.Session_t,
                   settings: inj.Settings_t) -> None:

    if len(post.content) > settings.comment_limit_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post payload exceeds the limit of {settings.comment_limit_size}"
        )

    elif len(post.content) < settings.comment_min_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post payload must be at least {settings.comment_min_size} characters"
        )

    await crud.set_post(session, current_user, post.content)


