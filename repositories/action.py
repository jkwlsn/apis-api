"""ActionRepository"""

from db.database_connection import DatabaseConnection
from models.action import Action


class ActionRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db: DatabaseConnection = db

    def create(self, notes: str, inspection_id: int) -> Action | None:
        query = "INSERT INTO actions (notes, inspection_id) VALUES (%s, %s) RETURNING action_id;"
        params: list[str | int] = [notes, inspection_id]
        results: list[Action] | None = self.db.execute(query, params)
        if results:
            return Action(results[0]["action_id"], notes, inspection_id)
        return None
