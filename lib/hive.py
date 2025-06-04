"""Hive model class"""

from dataclasses import dataclass


@dataclass
class Hive:
    """Class models system apiaries in the database"""

    hive_id: int
    name: str
    apiary_id: int

    def __str__(self) -> str:
        return f"Hive({self.hive_id}, {self.name}, {self.apiary_id})"
