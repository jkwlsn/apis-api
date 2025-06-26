"""Dependencies required by routes"""

from db.database_connection import DatabaseConnection
from repositories.apiary import ApiaryRepository
from repositories.user import UserRepository
from services.apiary import ApiaryService
from services.user import UserService


def get_user_service() -> UserService:
    db = DatabaseConnection()
    user_repo = UserRepository(db)
    return UserService(repo=user_repo)


def get_apiary_service() -> ApiaryService:
    db = DatabaseConnection()
    user_repo = UserRepository(db)
    apiary_repo = ApiaryRepository(db)
    return ApiaryService(apiary_repo=apiary_repo, user_repo=user_repo)
