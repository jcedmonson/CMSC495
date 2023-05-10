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
    posts: Mapped[list["UserPost"]] = relationship(back_populates="user_post")

class UserPost(Base):
    __tablename__ = "user_post"
    post_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_date: Mapped[datetime]
    content: Mapped[str] = mapped_column(String(2048))

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))

    user_post: Mapped["UserProfile"] = relationship(back_populates="posts")

    comments: Mapped[list["PostComment"]] = relationship(
        back_populates="comment_list", cascade="all, delete-orphan")

    reactions: Mapped[list["PostReaction"]] = relationship(
        back_populates="reaction_list", cascade="all, delete-orphan")

class UserConnection(Base):
    __tablename__ = "user_connection"
    current_user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))
    follows_user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))

    current_user = relationship("UserProfile", foreign_keys="[UserConnection.current_user_id]")
    follows_user = relationship("UserProfile", foreign_keys="[UserConnection.follows_user_id]")


    __table_args__ = (
        PrimaryKeyConstraint("current_user_id", "follows_user_id"),
    )

class PostComment(Base):
    __tablename__ = "post_comment"

    comment_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("user_post.post_id", ondelete="cascade"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id", ondelete="cascade"))
    user_name: Mapped[int] = mapped_column(ForeignKey("user_profile.user_name"))

    comment_date: Mapped[datetime]
    content: Mapped[str] = mapped_column(String(1024))

    comment_list: Mapped[UserPost] = relationship(back_populates="comments", cascade="delete")



class PostReaction(Base):
    __tablename__ = "post_reaction"
    post_id: Mapped[int] = mapped_column(ForeignKey("user_post.post_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id", ondelete="CASCADE"))
    user_name: Mapped[int] = mapped_column(ForeignKey("user_profile.user_name"))
    reaction_date: Mapped[datetime]
    reaction_id: Mapped[int]

    reaction_list: Mapped[UserPost] = relationship(back_populates="reactions", cascade="delete")

    __table_args__ = (
        PrimaryKeyConstraint("post_id", "user_id"),
    )


class Reactions(Base):
    """
    Table is a simple lookup of ID to some emoji/reaction character or
    something
    """
    __tablename__ = "reactions"

    reaction_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reaction_repr: Mapped[str]
