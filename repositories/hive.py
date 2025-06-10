"""HiveRepository"""

from db.database_connection import DatabaseConnection
from models.hive import Hive


class HiveRepository:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create(self, name: str, apiary_id: int) -> Hive | None:
        if len(name) and isinstance(apiary_id, int):
            query: str = (
                "INSERT INTO hives (name, apiary_id) VALUES (%s, %s) RETURNING hive_id;"
            )
            params: list = [name, apiary_id]
            results: list[dict] | None = self.db.execute(query, params)
            if results:
                return Hive(results[0]["hive_id"], name, apiary_id)
        return None

    def find_by_hive_id(self, hive_id: int) -> Hive | None:
        if isinstance(hive_id, int):
            query = "SELECT * FROM hives WHERE hive_id = %s LIMIT 1;"
            params = [hive_id]
            results = self.db.execute(query, params)
            if results:
                return Hive(
                    results[0]["hive_id"], results[0]["name"], results[0]["apiary_id"]
                )
        return None
