"""Inspection schema"""

from pydantic import AwareDatetime, BaseModel


class InspectionCreate(BaseModel):
    inspection_timestamp: AwareDatetime
    colony_id: int


class InspectionUpdate(BaseModel):
    inspection_timestamp: AwareDatetime
    colony_id: int


class InspectionRead(BaseModel):
    inspection_id: int
    inspection_timestamp: AwareDatetime
    colony_id: int
