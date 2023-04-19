from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status, Depends
from sqlalchemy import LargeBinary, String, select
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from .base import Base
from app_settings import Settings
from models import jwt_token_handler as jwt


class UserAccount(Base):
    __tablename__ = "user_account"

    user_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,
                                         index=True)

    user_name: Mapped[str] = mapped_column(String(30), nullable=False,
                                           unique=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(length=128),
                                                 nullable=False)

    user_creation_date: Mapped[datetime] = mapped_column(nullable=False)

    token: Mapped[str] = mapped_column(nullable=True)
    auth_creation_date: Mapped[datetime] = mapped_column(nullable=True)

    @classmethod
    async def login_user(cls,
                         session: AsyncSession,
                         settings: Settings,
                         user: UserLogin
                         ) -> UserAuthed | None:

        stmt = select(cls).where(cls.user_name == user.user_name)
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

    @classmethod
    async def create_user(cls,
                          session: AsyncSession,
                          settings: Settings,
                          user: UserCreate) -> UserAuthed | str:

        stmt = select(cls.user_name).where(
            cls.user_name == user.user_name or cls.email == user.email)

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
        new_user.token = jwt.create_access_token(settings, {"sub": new_user.user_name})
        new_user.auth_creation_date = datetime.utcnow()
        await session.commit()

        return UserAuthed(**new_user.__dict__)


class UserBase(BaseModel):
    user_name: str


class UserLogin(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserCreate(UserLogin):
    first_name: str
    last_name: str
    email: EmailStr


class UserAuthed(BaseModel):
    user_id: int
    user_name: str
    first_name: str
    last_name: str
    email: EmailStr
    token: str
