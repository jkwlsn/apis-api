"""Apiary model class"""

from dataclasses import dataclass


@dataclass
class Apiary:
    """Class models system apiaries in the database"""

    apiary_id: int
    name: str
    location: str
    user_id: int

    def __str__(self) -> str:
        return f"Apiary({self.apiary_id}, {self.name}, {self.location}, {self.user_id})"
