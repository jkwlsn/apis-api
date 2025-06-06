"""User repository"""

from db.database_connection import DatabaseConnection
from models.user import User


class UserRepository:
    """Controls the interaction between models.User and the database"""

    def __init__(self, database_connection: DatabaseConnection) -> None:
        """Init with a database connection"""
        self.db = database_connection

    def create(self, user: User) -> list[dict]:
        query: str = (
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;"
        )
        params: list[str] = [user.username, user.password]
        return self.db.execute(query, params)

    def find(self, user_id: int) -> list[dict]:
        query = "SELECT * FROM users WHERE user_id = %s;"
        params = [user_id]
        return self.db.execute(query, params)

    def read(self) -> list[dict]:
        query = "SELECT * FROM users;"
        return self.db.execute(query)

    def update(self, user_id: int, username: str, password: str) -> int:
        query = "UPDATE users SET username = %s, password = %s WHERE user_id = %s RETURNING user_id;"
        params = [username, password, user_id]
        return self.db.execute(query, params)

    def delete(self, user_id: int) -> bool:
        """Deletes a user by user_id. Returns True if the user was deleted, False otherwise"""
        query = "DELETE FROM users WHERE user_id = %s RETURNING user_id CASCADE;"
        params = [user_id]
        result = self.db.execute(query, params)
        return bool(result)
