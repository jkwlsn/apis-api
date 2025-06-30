"""Hive schema"""

from pydantic import BaseModel


class HiveCreate(BaseModel):
    name: str
    apiary_id: int


class HiveRead(BaseModel):
    hive_id: int
    name: str
    apiary_id: int


class HiveUpdate(BaseModel):
    name: str
    apiary_id: int
