"""Queen schema"""

from pydantic import BaseModel


class QueenCreate(BaseModel):
    colour: str
    clipped: bool
    colony_id: int


class QueenRead(BaseModel):
    queen_id: int
    colour: str
    clipped: bool
    colony_id: int
