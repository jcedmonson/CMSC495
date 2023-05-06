from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
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
    """
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True,
                                    index=True)

    user_name: Mapped[str] = mapped_column(String(30), nullable=False)


class User(BaseModel):
    user_id: int
    user_name: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserAuthed(User):
    account_status: bool
    account_private: bool
    email: EmailStr


