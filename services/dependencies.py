"""Dependencies required by routes"""

from db.instance import db
from repositories.apiary import ApiaryRepository
from repositories.colony import ColonyRepository
from repositories.hive import HiveRepository
from repositories.queen import QueenRepository
from repositories.user import UserRepository
from services.apiary import ApiaryService
from services.colony import ColonyService
from services.hive import HiveService
from services.queen import QueenService
from services.user import UserService


def get_user_service() -> UserService:
    user_repo = UserRepository(db)
    return UserService(repo=user_repo)


def get_apiary_service() -> ApiaryService:
    user_repo = UserRepository(db)
    apiary_repo = ApiaryRepository(db)
    return ApiaryService(apiary_repo=apiary_repo, user_repo=user_repo)


def get_hive_service() -> HiveService:
    apiary_repo = ApiaryRepository(db)
    hive_repo = HiveRepository(db)
    return HiveService(hive_repo=hive_repo, apiary_repo=apiary_repo)


def get_colony_service() -> ColonyService:
    colony_repo = ColonyRepository(db)
    hive_repo = HiveRepository(db)
    return ColonyService(colony_repo=colony_repo, hive_repo=hive_repo)


def get_queen_service() -> QueenService:
    queen_repo = QueenRepository(db)
    colony_repo = ColonyRepository(db)
    return QueenService(queen_repo=queen_repo, colony_repo=colony_repo)
