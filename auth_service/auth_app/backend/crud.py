import json
from datetime import datetime, timedelta
import logging

from fastapi import HTTPException, status
from httpx import AsyncClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_account import UserAccount, UserLogin, UserAuthed, UserCreate, \
    UserAcc
from app_settings import Settings
from backend import jwt_token_handler as jwt
import dependency_injection as inj


log = logging.getLogger("crud")

async def login_user(session: inj.Session_t,
                     settings: inj.Session_t,
                     user: UserLogin
                     ) -> UserAuthed | None:
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

    return UserAuthed(**user_db.__dict__)


async def create_user(session: inj.Session_t,
                      settings: inj.Settings_t,
                      user: UserCreate) -> UserAuthed | str:
    stmt = select(UserAccount.user_name).where(
        UserAccount.user_name == user.user_name or UserAccount.email == user.email)

    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is not None:
        return "Username already exists"

    new_user = user.dict()
    password_hash = jwt.get_password_hash(settings,
                                          new_user.pop("password"))

    new_user = UserAccount(**new_user, password_hash=password_hash,
                           user_creation_date=datetime.now())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    try:
        async with AsyncClient(base_url=settings.data_endpoint) as client:
            await client.post(
                "/sync_user",
                json=json.dumps(new_user.as_dict())
            )

    except Exception as error:
        log.error(f"Crud sync error: {error}")

    return UserAuthed(**new_user.__dict__)


async def get_user(session: AsyncSession, username: str) -> UserAccount:
    stmt = select(UserAccount).where(UserAccount.user_name == username)

    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


async def get_all_users(session: AsyncSession) -> list[UserAccount]:
    stmt = select(UserAccount)

    result = await session.execute(stmt)
    result = result.scalars().all()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


async def authenticate_user() -> UserAccount | bool:
    user = await get_user(session, username)
    if not user:
        return False

    if not jwt.verify_password(settings, password, user.password_hash):
        return False

    return user
