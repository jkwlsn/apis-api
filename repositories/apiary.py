"""ApiaryRepository"""

from db.database_connection import DatabaseConnection
from models.apiary import Apiary


class ApiaryRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create(self, name: str, location: str, user_id: int) -> Apiary | None:
        if len(name) and len(location) and isinstance(user_id, int):
            query: str = "INSERT INTO apiaries (name, location, user_id) VALUES (%s, %s, %s) RETURNING apiary_id;"
            params: list = [name, location, user_id]
            results: list[dict] | None = self.db.execute(query, params)
            if results:
                return Apiary(results[0]["apiary_id"], name, location, user_id)
        return None
