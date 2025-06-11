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

    def update(
        self, *, queen_id: int, colour: str, clipped: bool, colony_id: int
    ) -> Queen | None:
        query = "UPDATE queens SET colony_id = %s, colour = %s, clipped = %s WHERE queen_id = %s RETURNING queen_id;"
        params: list[str | int | bool] = [colony_id, colour, clipped, queen_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Queen(results[0]["queen_id"], colour, clipped, colony_id)
        return None

    def delete(self, queen_id: int) -> bool:
        query = "DELETE FROM queens WHERE queen_id = %s RETURNING queen_id;"
        params: list[int] = [queen_id]
        results: list[dict] | None = self.db.execute(query, params)
        return bool(results)
