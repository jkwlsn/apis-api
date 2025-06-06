"""Session repository"""

from db.database_connection import DatabaseConnection
from models.session import Session


class SessionRepository:
    """Controls the interaction between models.session and the database"""

    def __init__(self, database_connection: DatabaseConnection) -> None:
        """Init with a database connection"""
        self.db = database_connection

    def create(self, session: Session) -> list[dict]:
        query: str = "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s) RETURNING session_id;"
        params: list[str] = [session.session_start, session.user_id]
        return self.db.execute(query, params)

    def find_by_session_id(self, session_id: int) -> list[dict]:
        query = "SELECT * FROM sessions WHERE session_id = %s;"
        params = [session_id]
        return self.db.execute(query, params)

    def find_by_user_id(self, user_id: int) -> list[dict]:
        query = "SELECT * FROM sessions WHERE user_id = %s;"
        params = [user_id]
        return self.db.execute(query, params)

    def read(self) -> list[dict]:
        query = "SELECT * FROM sessions;"
        return self.db.execute(query)

    def update(self, session_id: int, session_start: str, user_id: str) -> int:
        query = "UPDATE sessions SET session_start = %s, user_id = %s WHERE session_id = %s RETURNING session_id;"
        params = [session_start, user_id, session_id]
        return self.db.execute(query, params)

    def delete(self, session_id: int) -> bool:
        """Deletes a session by session_id. Returns True if the session was deleted, False otherwise"""
        query = (
            "DELETE FROM sessions WHERE session_id = %s RETURNING session_id CASCADE;"
        )
        params = [session_id]
        result = self.db.execute(query, params)
        return bool(result)
