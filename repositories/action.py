"""ActionRepository"""

from db.database_connection import DatabaseConnection
from models.action import Action


class ActionRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db: DatabaseConnection = db

    def create(self, notes: str, inspection_id: int) -> Action | None:
        query: str = "INSERT INTO actions (notes, inspection_id) VALUES (%s, %s) RETURNING action_id;"
        params: list[str | int] = [notes, inspection_id]
        results: list[Action] | None = self.db.execute(query, params)
        if results:
            return Action(results[0]["action_id"], notes, inspection_id)
        return None

    def find_by_action_id(self, action_id: int) -> Action | None:
        query: str = "SELECT * FROM actions WHERE action_id = %s LIMIT 1;"
        params: list[int] = [action_id]
        results: list[Action] | None = self.db.execute(query, params)
        if results:
            return Action(
                results[0]["action_id"],
                results[0]["notes"],
                results[0]["inspection_id"],
            )
        return None

    def find_by_inspection_id(self, inspection_id: int) -> list[Action] | None:
        query: str = "SELECT * FROM actions WHERE inspection_id = %s;"
        params: list[int] = [inspection_id]
        results: list[Action] | None = self.db.execute(query, params)
        if results:
            return [
                Action(
                    row["action_id"],
                    row["notes"],
                    row["inspection_id"],
                )
                for row in results
            ]
        return None

    def read(self) -> list[Action] | None:
        query: str = "SELECT * FROM actions;"
        params: list = []
        results: list[Action] | None = self.db.execute(query, params)
        if results:
            return [
                Action(
                    row["action_id"],
                    row["notes"],
                    row["inspection_id"],
                )
                for row in results
            ]
        return None
