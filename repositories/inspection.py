"""InspectionRepository"""

from datetime import datetime

from db.database_connection import DatabaseConnection
from models.inspection import Inspection


class InspectionRepository:
    """Controls the interaction between models.inspection and the database"""

    def __init__(self, db: DatabaseConnection) -> None:
        """Init with a database connection"""
        self.db = db

    def create(
        self, inspection_timestamp: datetime, colony_id: int
    ) -> Inspection | None:
        query: str = "INSERT INTO inspections (inspection_timestamp, colony_id) VALUES (%s, %s) RETURNING inspection_id;"
        params: list[datetime | int] = [inspection_timestamp, colony_id]
        result: list[int] | None = self.db.execute(query, params)
        if result:
            return Inspection(
                result[0]["inspection_id"], inspection_timestamp, colony_id
            )
        return None

    def find_by_inspection_id(self, inspection_id: int) -> Inspection | None:
        query = "SELECT * FROM inspections WHERE inspection_id = %s LIMIT 1;"
        params = [inspection_id]
        results = self.db.execute(query, params)
        if results:
            return Inspection(
                results[0]["inspection_id"],
                results[0]["inspection_timestamp"],
                results[0]["colony_id"],
            )
        return None
