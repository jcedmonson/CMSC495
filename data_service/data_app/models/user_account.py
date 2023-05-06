from datetime import datetime

from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped

from pydantic import BaseModel, EmailStr

from models.base import Base


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

    account_status: Mapped[bool] = mapped_column(default=False)
    account_private: Mapped[bool] = mapped_column(default=False)

    token: Mapped[str] = mapped_column(nullable=True)
    auth_creation_date: Mapped[datetime] = mapped_column(nullable=True)


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


class User(BaseModel):
    user_id: int
    user_name: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserAcc(User):
    account_status: bool
    account_private: bool
    email: EmailStr


class UserAuthed(UserAcc):
    token: str | None

class UserSensitive(UserAuthed):
    password_hash: bytes
