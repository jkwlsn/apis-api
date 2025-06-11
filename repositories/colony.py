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

    def find_by_hive_id(self, hive_id: int) -> Colony | None:
        query: str = "SELECT * FROM colonies WHERE hive_id = %s LIMIT 1;"
        params: list = [hive_id]
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return Colony(results[0]["colony_id"], results[0]["hive_id"])
        return None

    def read(self) -> list[Colony] | None:
        query: str = "SELECT * FROM colonies;"
        params: list = []
        results: list[dict] | None = self.db.execute(query, params)
        if results:
            return [Colony(row["colony_id"], row["hive_id"]) for row in results]
        return None

    def update(self, colony_id: int, hive_id: int) -> Colony | None:
        if isinstance(hive_id, int):
            query: str = "UPDATE colonies SET hive_id = %s WHERE colony_id = %s RETURNING colony_id;"
            params: list[int] = [hive_id, colony_id]
            results: list[dict] = self.db.execute(query, params)
            if results:
                return Colony(results[0]["colony_id"], hive_id)
        return None

    def delete(self, colony_id: int) -> bool:
        query: str = "DELETE FROM colonies WHERE colony_id = %s"
        params: list[int] = [colony_id]
        results: list[dict] | None = self.db.execute(query, params)
        return bool(results)
