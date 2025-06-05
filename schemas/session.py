"""Session schema"""

from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    session_start: datetime
    user_id: int


class SessionRead(BaseModel):
    session_id: int
    session_start: datetime
    user_id: int
