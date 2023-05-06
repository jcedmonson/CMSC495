from datetime import datetime, timedelta
import logging
from typing import Any, Sequence

from fastapi import HTTPException, status

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession
import dependency_injection as inj
from models import sql_models
from models import padentic_models
from endpoints.auth import jwt_token_handler as jwt

log = logging.getLogger("crud")


async def login_user(session: inj.Session_t,
                     settings: inj.Session_t,
                     user: padentic_models.UserLogin
                     ) -> padentic_models.UserAuthed | None:
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

    return padentic_models.UserAuthed(**user_db.__dict__)


async def create_user(session: inj.Session_t,
                      settings: inj.Settings_t,
                      user: padentic_models.UserCreate) -> padentic_models.UserAuthed | str:
    stmt = select(sql_models.UserProfile.user_name).where(
        sql_models.UserProfile.user_name == user.user_name or sql_models.UserProfile.email == user.email)

    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is not None:
        return "Username already exists"

    new_user = user.dict()
    password_hash = jwt.get_password_hash(settings,
                                          new_user.pop("password"))

    new_user = sql_models.UserProfile(**new_user, password_hash=password_hash,
                                      user_creation_date=datetime.now())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return padentic_models.UserAuthed(**new_user.__dict__)


async def get_user(session: AsyncSession,
                   username: str) -> padentic_models.UserSensitive:
    stmt = select(sql_models.UserProfile).where(
        sql_models.UserProfile.user_name == username)

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
    stmt = select(sql_models.UserProfile)

    result = await session.execute(stmt)
    result = result.scalars().all()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


async def get_connections(session: AsyncSession,
                          user_id: int) -> list[padentic_models.User]:
    stmt = select(sql_models.UserProfile).where(
        sql_models.UserProfile.user_id == user_id)

    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User ID not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def authenticate_user(session, settings, username,
                            password) -> sql_models.UserProfile | bool:
    user = await get_user(session, username)
    if not user:
        return False

    if not jwt.verify_password(settings, password, user.password_hash):
        return False

    return user
