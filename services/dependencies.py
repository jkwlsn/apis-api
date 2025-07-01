"""Dependencies required by routes"""

from db.instance import db
from repositories.action import ActionRepository
from repositories.apiary import ApiaryRepository
from repositories.colony import ColonyRepository
from repositories.hive import HiveRepository
from repositories.inspection import InspectionRepository
from repositories.queen import QueenRepository
from repositories.user import UserRepository
from services.action import ActionService
from services.apiary import ApiaryService
from services.colony import ColonyService
from services.hive import HiveService
from services.inspection import InspectionService
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


def get_inspection_service() -> InspectionService:
    inspection_repo = InspectionRepository(db)
    colony_repo = ColonyRepository(db)
    return InspectionService(inspection_repo=inspection_repo, colony_repo=colony_repo)


def get_action_service() -> ActionService:
    action_repo = ActionRepository(db)
    inspection_repo = InspectionRepository(db)
    return ActionService(action_repo=action_repo, inspection_repo=inspection_repo)
