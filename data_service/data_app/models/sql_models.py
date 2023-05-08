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

class UserPost(Base):
    """
    Table represents the actual posts that a user has made

    Attributes
    ----------
    id: int
        Unique ID that represents the posts made by the user
    user_id: int
        ID of the user that made the posts
    post_date: datetime
        Datetime of the posts when it was made
    post: str
        Actual contents of the posts limited to 2048 bytes
    """
    __tablename__ = "user_post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))
    post_date: Mapped[datetime]
    post: Mapped[str] = mapped_column(String(2048))

    comments: Mapped[list["PostComment"]] = relationship(
        back_populates="comment_list", cascade="all, delete-orphan")
    reactions: Mapped[list["PostReaction"]] = relationship(
        back_populates="reaction_list", cascade="all, delete-orphan")


class PostComment(Base):
    """
    Table represents all the comments made to a posts

    Attributes
    ----------
    id: int
        Unique ID representing the comment made
    post_id: int
        ID of the posts the comment is commenting on
    user_id: int
        ID of the user that created the comment
    comment_date: datetime
        Date of when the comment was made
    comment: str
        Comment made with a limit of 1024 bytes
    """
    __tablename__ = "post_comment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("user_post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))
    comment_date: Mapped[datetime]
    comment: Mapped[str] = mapped_column(String(1024))

    comment_list: Mapped[UserPost] = relationship(back_populates="comments")


class PostReaction(Base):
    """
    Table represents the reaction the user had made to a comment. There is
    only one reaction a user can have to a posts.

    Attributes
    ----------
    post_id: int
        ID of the posts user is reacting to
    user_id: int
        User that is reacting to the posts
    reaction_date: datetime
        The date the user has reacted to the posts
    reaction_id: int
        ID that defines the unicode/character that the user reacted with
    """
    __tablename__ = "post_reaction"

    post_id: Mapped[int] = mapped_column(ForeignKey("user_post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.user_id"))
    reaction_date: Mapped[datetime]
    reaction_id: Mapped[int]

    reaction_list: Mapped[UserPost] = relationship(back_populates="reactions")

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
