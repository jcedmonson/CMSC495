from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


class UserProfile(Base):
    """
    Table represents the users public facing information

    Attributes
    ----------
    user_id: int
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

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(String(30))
    account_status: Mapped[bool] = mapped_column(default=False)
    account_private: Mapped[bool] = mapped_column(default=False)


class UserFriends(Base):
    __tablename__ = "user_friends"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    items: Mapped[list["Item"]] = relationship(back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(back_populates="items")
