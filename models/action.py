"""Action model class"""

from dataclasses import dataclass


@dataclass
class Action:
    """Models Actions in the database"""

    action_id: int
    notes: str
    inspection_id: int

    def __str__(self) -> str:
        return f"Action({self.action_id}, {self.notes}, {self.inspection_id})"
