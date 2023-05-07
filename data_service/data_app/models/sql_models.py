from datetime import datetime

from sqlalchemy import String, LargeBinary, PrimaryKeyConstraint, \
    ForeignKey, Table, Column

from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

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

    # Creates a one-to-many relationship with the connections table
    connections: Mapped[list["UserConnection"]] = relationship("UserConnection", foreign_keys="UserConnection.current_user_id", back_populates="current_user")

class UserConnection(Base):
    __tablename__ = "user_connection"
    current_user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))
    friend_with_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))

    current_user = relationship("UserProfile", foreign_keys="[UserConnection.current_user_id]")
    friend_with = relationship("UserProfile", foreign_keys="[UserConnection.friend_with_id]")


    __table_args__ = (
        PrimaryKeyConstraint("current_user_id", "friend_with_id"),
    )

# class UserConnection(Base):
#     """
#     Table represents all the user_ids that are actual friends with each other
#     """
#     __tablename__ = "user_connection"
#     connection_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     current_user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"), nullable=False)
#     friend_with_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"), nullable=False)
#
#     current_user: relationship("UserProfile", foreign_keys=[current_user_id])
#     friend_with: relationship("UserProfile", foreign_keys=[friend_with_id])
#
#     # __table_args__ = (
#     #     PrimaryKeyConstraint("current_user_id", "friend_with_id"),
#     # )
#
# association_table = Table(
#     "user_connection",
#     Base.metadata,
#     Column("current_user_id", ForeignKey("user_profile.user_id"), primary_key=True),
#     Column("friend_with_id", ForeignKey("user_profile.user_id"), primary_key=True),
# )
