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

    def find_by_observation_id(self, observation_id: int) -> Observation | None:
        query: str = "SELECT * FROM observations WHERE observation_id = %s LIMIT 1;"
        params: list[int] = [observation_id]
        results: list[Observation] | None = self.db.execute(query, params)
        if results:
            return Observation(
                results[0]["observation_id"],
                results[0]["queenright"],
                results[0]["queen_cells"],
                results[0]["bias"],
                results[0]["brood_frames"],
                results[0]["store_frames"],
                results[0]["chalk_brood"],
                results[0]["foul_brood"],
                results[0]["varroa_count"],
                results[0]["temper"],
                results[0]["notes"],
                results[0]["inspection_id"],
            )
        return None

    def find_by_inspection_id(self, inspection_id: int) -> Observation | None:
        query: str = "SELECT * FROM observations WHERE inspection_id = %s LIMIT 1;"
        params: list[int] = [inspection_id]
        results: list[Observation] | None = self.db.execute(query, params)
        if results:
            return Observation(
                results[0]["observation_id"],
                results[0]["queenright"],
                results[0]["queen_cells"],
                results[0]["bias"],
                results[0]["brood_frames"],
                results[0]["store_frames"],
                results[0]["chalk_brood"],
                results[0]["foul_brood"],
                results[0]["varroa_count"],
                results[0]["temper"],
                results[0]["notes"],
                results[0]["inspection_id"],
            )
        return None

    def read(self) -> list[Observation] | None:
        query: str = "SELECT * FROM observations;"
        params: list = []
        results: list[Observation] | None = self.db.execute(query, params)
        if results:
            return [
                Observation(
                    row["observation_id"],
                    row["queenright"],
                    row["queen_cells"],
                    row["bias"],
                    row["brood_frames"],
                    row["store_frames"],
                    row["chalk_brood"],
                    row["foul_brood"],
                    row["varroa_count"],
                    row["temper"],
                    row["notes"],
                    row["inspection_id"],
                )
                for row in results
            ]
        return None
