"""Inspection model class"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Inspection:
    """Models Inspections in the database"""

    inspection_id: int
    inspection_timestamp: datetime
    colony_id: int

    def __str__(self) -> str:
        return f"Inspection({self.inspection_id}, {self.inspection_timestamp}, {self.colony_id})"
