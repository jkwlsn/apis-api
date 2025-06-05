"""Inspection model class"""

import datetime
from dataclasses import dataclass


@dataclass
class Inspection:
    """Models Inspections in the database"""

    inspection_id: int
    inspection_timestamp: type[datetime.datetime]
    colony_id: int

    def __str__(self) -> str:
        return f"Inspection({self.inspection_id}, {self.inspection_timestamp}, {self.colony_id})"
