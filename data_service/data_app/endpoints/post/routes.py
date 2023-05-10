import logging

from fastapi import APIRouter, Header, status, HTTPException

from models import padentic_models as p_model
import dependency_injection as inj
from endpoints.auth.jwt_token_handler import CurrentUser_t
from endpoints import crud

log = logging.getLogger("endpoints.posts")
post_routes = APIRouter(prefix="/posts")

@post_routes.post("/delete/comment", status_code=201, summary="Remove a post that was posted by the user")
async def remove_comment(comment: p_model.RemoveComment,
                         current_user: CurrentUser_t,
                         session: inj.Session_t) -> None:

    await crud.remove_comment(session, current_user, comment)

@post_routes.post("/delete", summary="Remove a post", status_code=201)
async def remove_post(post: p_model.RemovePost,
                      current_user: CurrentUser_t,
                      session: inj.Session_t) -> None:

    
    await crud.remove_post(session, current_user, post)



@post_routes.get("/timeline/",
                 summary="Fetch all posts accessible by the current user ordered by newest")
async def get_all_posts(limit: int = 50,
                        offset: int = 0,
                        session: inj.Session_t = None,
                        current_user: CurrentUser_t = None
                        ) -> list[p_model.UserPost]:
    log.info(f"Fetching timeline for {current_user.user_name}")
    
    return await crud.get_all_posts(session, current_user, limit, offset)


@post_routes.post("/{post_id}/comment", status_code=201,
                  summary="Add comment to the post by post_id")
async def set_comment(post_id: int,
                      post_obj: p_model.PostCommentBody,
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

@post_routes.post("/{post_id}/reaction", status_code=201, summary="Add a reaction to the post by post_id")
async def set_comment(post_id: int,
                      reaction_obj: p_model.PostReaction,
                      current_user: CurrentUser_t,
                      session: inj.Session_t) -> None:

    log.debug(f"User {current_user.user_name} reacting to post id {post_id}")
    
    await crud.set_reaction(session, current_user, reaction_obj, post_id)

@post_routes.get("/{post_id}/{comment_id}", summary="Fetch a comment for the given post")
async def get_comment(post_id: int,
                      comment_id: int,
                      _: CurrentUser_t,
                      session: inj.Session_t) -> p_model.PostComment:
    log.debug(f"Fetching for comment {comment_id} from post {post_id}")
    
    return await crud.get_comment(session, post_id, comment_id)

@post_routes.get("/{post_id}", summary="Fetch post by ID")
async def get_post(post_id: int,
                   _: CurrentUser_t,
                   session: inj.Session_t) -> p_model.UserPost:

    
    return await crud.get_post(session, post_id)





@post_routes.get("", summary="Fetch all posts made by current user")
async def get_posts(current_user: CurrentUser_t,
                    session: inj.Session_t
                    ) -> list[p_model.UserPost]:

    log.debug(f"Querying posts for {current_user.user_name}")
    result = await crud.get_posts(session, current_user)
    
    return result


@post_routes.post("", status_code=201, summary="Submit a new post")
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
