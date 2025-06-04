"""Queen model class"""

from dataclasses import dataclass


@dataclass
class Colony:
    """Models queens in the database"""

    queen_id: int
    colour: str
    clipped: bool
    colony_id: int

    def __str__(self) -> str:
        return (
            f"Colony({self.colony_id}, {self.colour}, {self.clipped}, {self.colony_id})"
        )
