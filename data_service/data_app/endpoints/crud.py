from datetime import datetime, timedelta
import logging
from typing import Any, Sequence

from fastapi import HTTPException, status

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import dependency_injection as inj
from models.sql_models import UserProfile, UserConnection, UserPost, \
    PostComment
from models import padentic_models as p_model
from endpoints.auth import jwt_token_handler as jwt

log = logging.getLogger("crud")


def set_post_model(post: tuple[UserPost, UserProfile]) -> p_model.UserPost:
    post, user = post
    return p_model.UserPost(
        user_id=user.user_id,
        user_name=user.user_name,
        first_name=user.first_name,
        last_name=user.last_name,

        post_id=post.post_id,
        post_date=post.post_date,
        content=post.content,
        comments=post.comments,
        reactions=post.reactions
    )

def set_post_models(posts: list[tuple[UserPost, UserProfile]]) -> list[p_model.UserPost]:
    post_objs = []
    for post in posts:
        post_objs.append(set_post_model(post))
    return post_objs



async def login_user(session: inj.Session_t,
                     settings: inj.Session_t,
                     user: p_model.UserLogin
                     ) -> p_model.UserAuthed | None:
    try:
        user_db = await get_user(session, user.user_name)
    except:
        raise

    if not jwt.verify_password(settings,
                               user.password,
                               user_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)

    access_token = jwt.create_access_token(
        data={"sub": user_db.user_name},
        settings=settings,
        expires_delta=access_token_expires
    )

    user_db.token = access_token
    await session.commit()
    await session.refresh(user_db)

    return p_model.UserAuthed(**user_db.__dict__)


async def create_user(session: inj.Session_t,
                      settings: inj.Settings_t,
                      user: p_model.UserCreate) -> p_model.UserAuthed | str:
    stmt = select(UserProfile.user_name).where(
        UserProfile.user_name == user.user_name or UserProfile.email == user.email)

    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is not None:
        return "Username already exists"

    new_user = user.dict()
    password_hash = jwt.get_password_hash(settings,
                                          new_user.pop("password"))

    new_user = UserProfile(**new_user, password_hash=password_hash,
                           user_creation_date=datetime.now())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return p_model.UserAuthed(**new_user.__dict__)


async def get_user(session: AsyncSession, username: str,
                   exact_match: bool = True):
    stmt = select(UserProfile).filter(
        UserProfile.user_name.ilike(f"%{username}%"))

    result = await session.execute(stmt)
    result = result.scalars().all()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if exact_match:
        if len(result) > 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find an exact query match",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return result[0]

    return result


async def get_all_users(session: AsyncSession) -> Sequence[
    Row | RowMapping | Any]:
    stmt = select(UserProfile)

    result = await session.execute(stmt)
    result = result.scalars().all()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


async def get_user_by_id(session: AsyncSession,
                         user_id: int) -> p_model.User:
    log.debug(f"Fetching user {user_id}")

    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        log.debug(f"Unable to fetch user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User ID not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    log.debug(f"Fetched user {result}")
    return result


async def get_connections(session: AsyncSession,
                          user_id: int) -> list[UserProfile]:
    # If successful, the user exists
    try:
        _ = await get_user_by_id(session, user_id)
    except:
        raise

    # Select all the connection IDs that the user has
    stmt = select(UserConnection).where(
        UserConnection.current_user_id == user_id)
    result = await session.execute(stmt)

    # get the ID of the users the user has a connection with
    connections = [i.follows_user_id for i in result.scalars().all()]
    log.debug(f"User {user_id} has {len(connections)} connections")

    # Fetch all the users from the given IDs
    stmt = select(UserProfile).where(UserProfile.user_id.in_(connections))
    result = await session.execute(stmt)
    connections = result.scalars().all()

    return connections


async def set_comment(session: AsyncSession,
                      current_user: p_model.UserAuthed,
                      post_obj: p_model.PostComment,
                      post_id: int):

    stmt = (
        select(UserPost)
        .options(selectinload(UserPost.comments),
                 selectinload(UserPost.reactions))
        .where(UserPost.post_id == post_id)
    )

    result = await session.execute(stmt)
    post: UserPost = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post ID {post_id} was not found"
        )

    new_post = PostComment(
        post_id=post.post_id,
        user_id=current_user.user_id,
        comment_date=datetime.utcnow(),
        comment=post.content
    )

    import ipdb;ipdb.set_trace()

    post.comments.append(new_post)


    import ipdb;ipdb.set_trace()
    await session.commit()


async def get_all_posts(session: AsyncSession, limit: int, offset: int):
    stmt = (
        select(UserPost, UserProfile)
        .join(UserProfile)
        .options(selectinload(UserPost.comments),
                 selectinload(UserPost.reactions))
        .order_by(UserPost.post_date.desc())
        .offset(offset)
        .limit(limit)
    )

    posts = (await session.execute(stmt)).all()
    return set_post_models(posts)


async def get_post(session: AsyncSession, post_id: int):
    stmt = (
        select(UserPost, UserProfile)
        .join(UserProfile)
        .options(selectinload(UserPost.comments),
                 selectinload(UserPost.reactions))
        .where(UserPost.user_id == post_id)
    )

    post = (await session.execute(stmt)).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post was not found"
        )

    return set_post_model(post)

async def get_posts(session: AsyncSession,
                    current_user: p_model.UserAuthed) -> list[p_model.UserPost]:
    stmt = (
        select(UserPost, UserProfile)
        .join(UserProfile)
        .where(UserPost.user_id == current_user.user_id)
        .options(selectinload(UserPost.comments),
                 selectinload(UserPost.reactions))
        .order_by(UserPost.post_date.desc())
    )

    posts = (await session.execute(stmt)).all()
    return set_post_models(posts)

    # stmt = select(UserProfile).where(
    #     UserProfile.user_id == current_user.user_id).options(
    #     selectinload(UserProfile.posts))
    # result = await session.execute(stmt)
    # user = result.scalar_one_or_none()
    #
    # if user is None or not user.posts:
    #     return []
    #
    # posts = []
    # user_model = p_model.User.from_orm(user)
    # for post in user.posts:
    #     post = p_model.UserPost(
    #         user_id=user_model.user_id,
    #         post_id=post.post_id,
    #         post_date=post.post_date,
    #         user_name=user_model.user_name,
    #         first_name=user_model.first_name,
    #         last_name=user_model.last_name,
    #         content=post.content,
    #     )
    #     posts.append(post)
    # return posts
    #
    #
async def set_post(session: AsyncSession, current_user: p_model.UserAuthed,
                   post_body: str):
    post = UserPost(content=post_body,
                    user_id=current_user.user_id,
                    post_date=datetime.utcnow())
    session.add(post)
    await session.commit()


async def set_connection(session: AsyncSession,
                         current_user: p_model.UserAuthed,
                         user_to_follow: p_model.User) -> None:
    # If this is successful, then the user being added is an actual user
    try:
        _ = await get_user_by_id(session, user_to_follow.user_id)
    except:
        raise

    # Fetch previous connections for testing later
    prev = await get_connections(session, current_user.user_id)

    # Add the connection between users
    try:
        session.add(UserConnection(current_user_id=current_user.user_id,
                                   follows_user_id=user_to_follow.user_id))
        await session.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Connection between users already exists",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Query to ensure that the connection was added
    result = await get_connections(session, current_user.user_id)

    if len(prev) == len(result):
        log.error(
            f"Failed to add connection {current_user.user_id} -> {user_to_follow.user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add connection between users",
            headers={"WWW-Authenticate": "Bearer"}
        )

    log.debug(
        f"Connection {current_user.user_id} -> {user_to_follow.user_id} made")


async def authenticate_user(session, settings, username,
                            password) -> UserProfile | bool:
    user = await get_user(session, username)
    if not user:
        return False

    if not jwt.verify_password(settings, password, user.password_hash):
        return False

    return user
