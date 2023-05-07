from datetime import datetime, timedelta
import logging
from typing import Any, Sequence

from fastapi import HTTPException, status

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession
import dependency_injection as inj
from models.sql_models import UserProfile, UserConnection
from models import padentic_models as p_model
from endpoints.auth import jwt_token_handler as jwt

log = logging.getLogger("crud")


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


async def get_user(session: AsyncSession,
                   username: str) -> p_model.UserSensitive:
    stmt = select(UserProfile).where(
        UserProfile.user_name == username)

    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User ID not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result

async def get_connections(session: AsyncSession,
                          user_id: int) -> list[p_model.User]:
    # If successful, the user exists
    try:
        _ = get_user_by_id(session, user_id)
    except:
        raise

    stmt = select(UserConnection).where(UserConnection.current_user_id == user_id)
    result = await session.execute(stmt)
    return [p_model.User(**i) for i in result.scalars().all() ]

async def set_connection(session: AsyncSession,
                         current_user: p_model.UserAuthed,
                         user_to_follow: p_model.User) -> None:

    # If this is successful, then the user being added is an actual user
    try:
        _ = get_user_by_id(session, user_to_follow.user_id)
    except:
        raise

    # Fetch previous connections for testing later
    prev = await get_connections(session, current_user.user_id)

    # Add the connection between users
    session.add(UserConnection(current_user_id=current_user.user_id, follows_user_id=user_to_follow.user_id))
    await session.commit()

    # Query to ensure that the connection was added
    stmt = select(UserConnection).where(UserConnection.current_user_id == current_user.user_id)
    result = await session.execute(stmt)
    result = result.scalars().all()

    if len(prev) == len(result):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add connection between users",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def authenticate_user(session, settings, username,
                            password) -> UserProfile | bool:
    user = await get_user(session, username)
    if not user:
        return False

    if not jwt.verify_password(settings, password, user.password_hash):
        return False

    return user
