"""Inspection schema"""

from datetime import datetime

from pydantic import BaseModel


class InspectionCreate(BaseModel):
    inspection_timestamp: datetime
    colony_id: int


class InspectionRead(BaseModel):
    inspection_id: int
    inspection_timestamp: datetime
    colony_id: int
