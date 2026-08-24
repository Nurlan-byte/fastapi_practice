from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostOut(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    model_config = ConfigDict(from_attributes=True)


class PostVoteOut(BaseModel):
    Post: PostOut
    votes: int

    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class Vote(BaseModel):
    post_id: int
    sign: Literal[0, 1]
