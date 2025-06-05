"""Observation model class"""

from dataclasses import dataclass


@dataclass
class Observation:
    """Models Observations in the database"""

    observation_id: int
    queenright: bool
    queen_cells: int
    bias: bool
    brood_frames: int
    store_frames: int
    chalk_brood: bool
    foul_brood: bool
    varroa_count: int
    temper: int
    notes: str
    inspection_id: int

    def __str__(self) -> str:
        return f"Observation({self.observation_id}, {self.queenright}, {self.queen_cells}, {self.bias}, {self.brood_frames}, {self.store_frames}, {self.chalk_brood}, {self.foul_brood}, {self.varroa_count}, {self.temper}, {self.notes}, {self.inspection_id})"
