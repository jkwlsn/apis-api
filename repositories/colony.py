"""ColonyRepository"""

from db.database_connection import DatabaseConnection
from models.colony import Colony


class ColonyRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create(self, hive_id: int) -> Colony | None:
        query: str = "INSERT INTO colonies (hive_id) VALUES (%s) RETURNING colony_id;"
        params: list = [hive_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Colony(results[0]["colony_id"], hive_id)
        return None

    def find_by_colony_id(self, colony_id: int) -> Colony | None:
        query: str = "SELECT * FROM colonies WHERE colony_id = %s LIMIT 1;"
        params: list = [colony_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Colony(results[0]["colony_id"], results[0]["hive_id"])
        return None
