"""Apiary schema"""

from pydantic import BaseModel


class ApiaryCreate(BaseModel):
    name: str
    location: str
    user_id: int


class ApiaryRead(BaseModel):
    apiary_id: int
    name: str
    location: str
    user_id: int
