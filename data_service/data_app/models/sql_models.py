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
    follows_user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))

    current_user = relationship("UserProfile", foreign_keys="[UserConnection.current_user_id]")
    follows_user = relationship("UserProfile", foreign_keys="[UserConnection.follows_user_id]")


    __table_args__ = (
        PrimaryKeyConstraint("current_user_id", "follows_user_id"),
    )

