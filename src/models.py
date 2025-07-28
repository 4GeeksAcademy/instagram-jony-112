from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, Table, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import enum


db = SQLAlchemy()


class MediaType (enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="user")
    comment: Mapped["Comment"] = relationship(back_populates="user")
    follower: Mapped["Follower"] = relationship(back_populates="user_to")
    following: Mapped["Follower"] = relationship(back_populates="user_from")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.firstname,
            "last_name": self.lastname,
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="post")
    media: Mapped["Media"] = relationship(back_populates="post")
    comment: Mapped["Comment"] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comment")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comment")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user_from: Mapped["User"] = relationship(
        "User", foreign_keys=[user_from_id], back_populates="following"
    )
    user_to: Mapped["User"] = relationship(
        "User", foreign_keys=[user_to_id], back_populates="follower"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }