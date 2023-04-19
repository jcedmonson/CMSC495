from datetime import datetime

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base


class UserFriends(Base):
    """
    Table represents all the user_ids that are actual friends with each other
    """
    __tablename__ = "user_friend"
    current_user: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    friend_with: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))

    __table_args__ = (
        PrimaryKeyConstraint("current_user", "friend_with"),
    )


class UserPost(Base):
    """
    Table represents the actual posts that a user has made

    Attributes
    ----------
    id: int
        Unique ID that represents the post made by the user
    user_id: int
        ID of the user that made the post
    post_date: datetime
        Datetime of the post when it was made
    post: str
        Actual contents of the post limited to 2048 bytes
    """
    __tablename__ = "user_post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    post_date: Mapped[datetime]
    post: Mapped[str] = mapped_column(String(2048))

    comments: Mapped[list["PostComment"]] = relationship(
        back_populates="comment_list", cascade="all, delete-orphan")
    reactions: Mapped[list["PostReaction"]] = relationship(
        back_populates="reaction_list", cascade="all, delete-orphan")


class PostComment(Base):
    """
    Table represents all the comments made to a post

    Attributes
    ----------
    id: int
        Unique ID representing the comment made
    post_id: int
        ID of the post the comment is commenting on
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
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    comment_date: Mapped[datetime]
    comment: Mapped[str] = mapped_column(String(1024))

    comment_list: Mapped[UserPost] = relationship(back_populates="comments",
                                                  cascade="all, delete-orphan")


class PostReaction(Base):
    """
    Table represents the reaction the user had made to a comment. There is
    only one reaction a user can have to a post.

    Attributes
    ----------
    post_id: int
        ID of the post user is reacting to
    user_id: int
        User that is reacting to the post
    reaction_date: datetime
        The date the user has reacted to the post
    reaction_id: int
        ID that defines the unicode/character that the user reacted with
    """
    __tablename__ = "post_reaction"

    post_id: Mapped[int] = mapped_column(ForeignKey("user_post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    reaction_date: Mapped[datetime]
    reaction_id: Mapped[int]

    reaction_list: Mapped[UserPost] = relationship(back_populates="reactions",
                                                   cascade="all, delete-orphan")

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
