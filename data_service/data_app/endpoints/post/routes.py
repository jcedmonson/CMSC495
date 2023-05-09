import logging

from fastapi import APIRouter, Header, status, HTTPException

from models import padentic_models as p_model
import dependency_injection as inj
from endpoints.auth.jwt_token_handler import CurrentUser_t
from endpoints import crud

log = logging.getLogger("endpoints.posts")
post_routes = APIRouter(prefix="/posts")


@post_routes.get("/{post_id}",
                 summary="Fetch a post based on the ID of the post")
async def get_post(post_id: int,
                   _: CurrentUser_t,
                   session: inj.Session_t) -> p_model.UserPost:
    return await crud.get_post(session, post_id)


@post_routes.post("/{post_id}/comment", status_code=201,
                  summary="Create a comment on a post")
async def set_comment(post_id: int,
                      post_obj: p_model.PostComment,
                      current_user: CurrentUser_t,
                      session: inj.Session_t,
                      settings: inj.Settings_t) -> None:
    if len(post_obj.content) > settings.comment_limit_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post payload exceeds the limit of {settings.comment_limit_size}"
        )

    elif len(post_obj.content) < settings.comment_min_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Comment payload must be at least {settings.comment_min_size} characters"
        )
    await crud.set_comment(session, current_user, post_obj, post_id)


@post_routes.get("/timeline/",
                 summary="Fetch all posts ordered by newest posts. Default limit is 50 with an offset of 0")
async def get_all_posts(limit: int = 50,
                        offset: int = 0,
                        session: inj.Session_t = None
                        ) -> list[p_model.UserPost]:
    return await crud.get_all_posts(session, limit, offset)


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
    if len(post.content) > settings.post_limit_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post payload exceeds the limit of {settings.post_limit_size}"
        )

    elif len(post.content) < settings.post_min_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post payload must be at least {settings.post_min_size} characters"
        )
    await crud.set_post(session, current_user, post.content)
