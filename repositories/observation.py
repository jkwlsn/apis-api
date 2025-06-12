"""ObservationRepository"""

from db.database_connection import DatabaseConnection
from models.observation import Observation


class ObservationRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db: DatabaseConnection = db

    def create(
        self,
        *,
        queenright: bool,
        queen_cells: int,
        bias: bool,
        brood_frames: int,
        store_frames: int,
        chalk_brood: bool,
        foul_brood: bool,
        varroa_count: int,
        temper: int,
        notes: str,
        inspection_id: int,
    ) -> Observation | None:
        query: str = "INSERT INTO observations (queenright, queen_cells, bias, brood_frames, store_frames, chalk_brood, foul_brood, varroa_count, temper, notes, inspection_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING observation_id;"
        params: list[str | int] = [
            queenright,
            queen_cells,
            bias,
            brood_frames,
            store_frames,
            chalk_brood,
            foul_brood,
            varroa_count,
            temper,
            notes,
            inspection_id,
        ]
        results: list[Observation] | None = self.db.execute(query, params)
        if results:
            return Observation(
                results[0]["observation_id"],
                queenright,
                queen_cells,
                bias,
                brood_frames,
                store_frames,
                chalk_brood,
                foul_brood,
                varroa_count,
                temper,
                notes,
                inspection_id,
            )
        return None
