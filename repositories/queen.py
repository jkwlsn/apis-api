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

    def find_by_queen_id(self, queen_id: int) -> Queen | None:
        query = "SELECT * FROM queens WHERE queen_id = %s LIMIT 1;"
        params: list[int] = [queen_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Queen(
                results[0]["queen_id"],
                results[0]["colour"],
                results[0]["clipped"],
                results[0]["colony_id"],
            )
        return None

    def find_by_colony_id(self, queen_id: int) -> Queen | None:
        query = "SELECT * FROM queens WHERE colony_id = %s LIMIT 1;"
        params: list[int] = [queen_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Queen(
                results[0]["queen_id"],
                results[0]["colour"],
                results[0]["clipped"],
                results[0]["colony_id"],
            )
        return None

    def read(self) -> list[Queen] | None:
        query = "SELECT * FROM queens;"
        params: list = []
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return [
                Queen(
                    row["queen_id"],
                    row["colour"],
                    row["clipped"],
                    row["colony_id"],
                )
                for row in results
            ]
        return None
