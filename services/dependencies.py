"""Dependencies required by routes"""

from db.database_connection import DatabaseConnection
from repositories.user import UserRepository
from services.user import UserService


def get_user_service() -> UserService:
    repo = UserRepository(db=DatabaseConnection)
    return UserService(repo=repo)
