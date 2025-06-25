"""User schema"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    user_id: int
    username: str
    password: str
