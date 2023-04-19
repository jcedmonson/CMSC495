from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user_account import UserAccount, UserLogin, UserAuthed, UserCreate
from backend import jwt_token_handler as jwt
from app_settings import Settings


async def login_user(session: AsyncSession,
                     settings: Settings,
                     user: UserLogin
                     ) -> UserAuthed | None:
    stmt = select(UserAccount).where(UserAccount.user_name == user.user_name)
    result = await session.execute(stmt)
    user_db = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not jwt.verify_password(settings, user.password,
                               user_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = jwt.create_access_token(settings, {"user": user_db.user_name})
    return UserAuthed(**user_db._mapping, token=token)


async def create_user(session: AsyncSession,
                      settings: Settings,
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

    # Returned the "authed user
    new_user.token = jwt.create_access_token(settings,
                                             {"sub": new_user.user_name})
    new_user.auth_creation_date = datetime.utcnow()
    await session.commit()

    return UserAuthed(**new_user.__dict__)


async def get_user(user: str,
                   session: AsyncSession):
    stmt = select(UserAccount.user_name).where(UserAccount.user_name == user)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")
