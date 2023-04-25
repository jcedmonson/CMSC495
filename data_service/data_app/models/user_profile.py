from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from .base import Base


class UserProfile(Base):
    """
    Table represents the users public facing information

    Attributes
    ----------
    id: int
        Unique ID automatically given to the user
    user_name: str
        User chosen name
    account_status: bool
        Indicate if the user is "active". A true value indicates that the user
        is in fact "active", while a false indicates that the user is
        "inactive".
    account_private: bool
        Bool indicates if the account is private (True) requiring guest
        user to be friends with the user
    """
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,
                                    index=True)

    user_name: Mapped[str] = mapped_column(String(30), nullable=False)
    account_status: Mapped[bool] = mapped_column(default=False)
    account_private: Mapped[bool] = mapped_column(default=False)

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

# class LoginUser(BaseUser):
#     password: str
#
# class UserProfile(BaseModel):
#     id: int
#     user_name: str
#
# class UserProfileAll(UserProfile):
#     account_status: bool
#     account_private: bool
#
# class PostComment(UserProfile):
#     id: int
#     post_id: int
#     user_id: int
#
# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         orm_mode = True
#
#
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []
#
#     class Config:
#         orm_mode = True
