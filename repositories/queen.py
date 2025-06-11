"""QueenRepository"""

from db.database_connection import DatabaseConnection
from models.queen import Queen


class QueenRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db: DatabaseConnection = db

    def create(self, *, colour: str, clipped: bool, colony_id: int) -> Queen | None:
        query: str = "INSERT INTO queens (colour, clipped, colony_id) VALUES (%s, %s, %s) RETURNING queen_id;"
        params: list[str | bool | int] = [colour, clipped, colony_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Queen(results[0]["queen_id"], colour, clipped, colony_id)
        return None
