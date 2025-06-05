"""Action schema"""

from pydantic import BaseModel


class ActionCreate(BaseModel):
    notes: str
    inspection_id: int


class ActionRead(BaseModel):
    action_id: int
    notes: str
    inspection_id: int
