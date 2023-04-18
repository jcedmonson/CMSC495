from __future__ import annotations

from datetime import datetime

from sqlalchemy import LargeBinary, String, select
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
import bcrypt

from .base import Base


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,
                                    index=True)

    user_name: Mapped[str] = mapped_column(String(30), nullable=False,
                                           unique=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(length=128), nullable=False)

    user_creation_date: Mapped[datetime] = mapped_column(nullable=False)

    auth_token: Mapped[str] = mapped_column(nullable=True)
    auth_creation_date: Mapped[datetime] = mapped_column(nullable=True)

    @staticmethod
    def get_hashed_password(plain_text_password: str) -> bytes:
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode(encoding="UTF-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password, hashed_password)

    @classmethod
    async def login_user(cls,
                         session: AsyncSession,
                         user_name: str,
                         password: str
                         ) -> None:
        stmt = select(cls).where(cls.user_name == user_name)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            return None

    @classmethod
    async def create_user(cls,
                          session: AsyncSession,
                          user: UserCreate) -> str:

        stmt = select(cls.user_name).where(
            cls.user_name == user.user_name or cls.email == user.email)

        result = await session.execute(stmt)
        result = result.scalar_one_or_none()

        if result is not None:
            return "Username already exists"

        new_user = user.dict()
        password_hash = cls.get_hashed_password(new_user.pop("password"))
        new_user = UserAccount(**new_user, password_hash=password_hash, user_creation_date=datetime.now())
        session.add(new_user)
        await session.commit()

        # import ipdb; ipdb.set_trace()

        return "User added?"


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
    auth_token: str
