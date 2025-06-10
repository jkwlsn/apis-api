"""User repository"""

from db.database_connection import DatabaseConnection
from models.user import User


class UserRepository:
    """Controls the interaction between models.User and the database"""

    def __init__(self, db: DatabaseConnection) -> None:
        """Init with a database connection"""
        self.db = db

    def create(self, username: str, password: str) -> User | None:
        if len(username) > 0 and len(password) > 0:
            query: str = "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;"
            params: list[str] = [username, password]
            results = self.db.execute(query, params)
            if results:
                return User(
                    user_id=results[0]["user_id"], username=username, password=password
                )
        return None

    def find(self, user_id: int) -> User | None:
        query = "SELECT * FROM users WHERE user_id = %s LIMIT 1;"
        params = [user_id]
        results = self.db.execute(query, params)
        if results:
            return User(
                user_id=results[0]["user_id"],
                username=results[0]["username"],
                password=results[0]["password"],
            )
        return None

    def read(self) -> list[User] | None:
        query = "SELECT * FROM users;"
        params = []
        results = self.db.execute(query, params)
        if results:
            return [
                User(
                    user_id=row["user_id"],
                    username=row["username"],
                    password=row["password"],
                )
                for row in results
            ]
        return None

    def update(self, user_id: int, username: str, password: str) -> User | None:
        query = "UPDATE users SET username = %s, password = %s WHERE user_id = %s RETURNING user_id;"
        params = [username, password, user_id]
        results = self.db.execute(query, params)
        if results:
            return User(
                user_id=results[0]["user_id"],
                username=results[0]["username"],
                password=results[0]["password"],
            )
        return None

    def delete(self, user_id: int) -> bool:
        """Deletes a user by user_id. Returns True if the user was deleted, False otherwise"""
        query = "DELETE FROM users WHERE user_id = %s RETURNING user_id;"
        params = [user_id]
        result = self.db.execute(query, params)
        return bool(result)
