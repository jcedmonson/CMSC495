from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, select
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from .base import Base


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,
                                    index=True)

    user_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    user_creation_date: Mapped[datetime] = mapped_column(nullable=False)

    auth_token: Mapped[str]
    auth_creation_date: Mapped[datetime]

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


class UserBase(BaseModel):
    user_name: str


class UserLogin(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserCreate(UserLogin):
    email: EmailStr


class UserAuthed(BaseModel):
    user_id: int
    user_name: str
    auth_token: str

