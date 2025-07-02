"""Observation schema"""

from pydantic import BaseModel


class ObservationCreate(BaseModel):
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


class ObservationUpdate(BaseModel):
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


class ObservationRead(BaseModel):
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
