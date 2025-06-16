"""Session repository"""

from datetime import datetime

from db.database_connection import DatabaseConnection
from models.session import Session


class SessionRepository:
    """Controls the interaction between models.session and the database"""

    def __init__(self, database_connection: DatabaseConnection) -> None:
        """Init with a database connection"""
        self.db = database_connection

    def create(self, session_start: datetime, user_id: int) -> Session | None:
        query: str = "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s) RETURNING session_id;"
        params: list[datetime | int] = [session_start, user_id]
        result: list[int] | None = self.db.execute(query, params)
        if result:
            return Session(result[0]["session_id"], session_start, user_id)
        return None

    def find_by_session_id(self, session_id: int) -> Session | None:
        query = "SELECT * FROM sessions WHERE session_id = %s LIMIT 1;"
        params = [session_id]
        results = self.db.execute(query, params)
        if results:
            return Session(
                results[0]["session_id"],
                results[0]["session_start"],
                results[0]["user_id"],
            )
        return None

    def find_by_user_id(self, user_id: int) -> list[Session] | None:
        query = "SELECT * FROM sessions WHERE user_id = %s;"
        params = [user_id]
        results = self.db.execute(query, params)
        if results:
            return [
                Session(row["session_id"], row["session_start"], row["user_id"])
                for row in results
            ]
        return None

    def read(self) -> list[Session] | None:
        query = "SELECT * FROM sessions;"
        params = []
        results = self.db.execute(query, params)
        if results:
            return [
                Session(row["session_id"], row["session_start"], row["user_id"])
                for row in results
            ]
        return None

    def delete_by_session_id(self, session_id: int) -> bool:
        """Deletes a session by session_id. Returns True if the session was deleted, False otherwise"""
        query = "DELETE FROM sessions WHERE session_id = %s RETURNING session_id;"
        params = [session_id]
        result = self.db.execute(query, params)
        return bool(result)

    def delete_by_user_id(self, session_id: int) -> bool:
        """Deletes a session by user_id. Returns True if the user_id exists, false otherwise."""
        query = "DELETE FROM sessions WHERE user_id = %s RETURNING user_id;"
        params = [session_id]
        result = self.db.execute(query, params)
        return bool(result)
