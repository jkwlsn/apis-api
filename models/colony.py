"""Colony model class"""

from dataclasses import dataclass


@dataclass
class Colony:
    """Class models colonies in the database"""

    colony_id: int
    hive_id: int

    def __str__(self) -> str:
        return f"Colony({self.colony_id}, {self.hive_id})"
