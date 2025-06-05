"""Queen model class"""

from dataclasses import dataclass


@dataclass
class Queen:
    """Models queens in the database"""

    queen_id: int
    colour: str
    clipped: bool
    colony_id: int

    def __str__(self) -> str:
        return (
            f"Queen({self.queen_id}, {self.colour}, {self.clipped}, {self.colony_id})"
        )
