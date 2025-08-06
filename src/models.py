from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Column, Table, ForeignKey, Integer
from typing import List
from sqlalchemy import DateTime, func
from sqlalchemy import Enum

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    followers: Mapped[List["Follower"]] = relationship(
        foreign_keys="[Follower.user_to_id]")
    following: Mapped[List["Follower"]] = relationship(
        foreign_keys="[Follower.user_from_id]")
    comments: Mapped[List["Comment"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user_from: Mapped["User"] = relationship(foreign_keys=[user_from_id])
    user_to: Mapped["User"] = relationship(foreign_keys=[user_to_id])

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comments: Mapped[List["Comment"]] = relationship()

def serialize(self):
    return {
        "user_id": self.user_id
    }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    post: Mapped["Post"] = relationship()
    user: Mapped["User"] = relationship()

    def serialize(self):
        return{
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "comment_text": self.content,
            "created_at": self.created_at
        }

class MediaType(str, Enum):
    imagen = "imagen"
    video = "video"

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(db.String(10), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship()

    def serialize(self):
        return{
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }