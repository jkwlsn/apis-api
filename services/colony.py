"""ColonyService"""

from models.colony import Colony
from repositories.colony import ColonyRepository
from repositories.hive import HiveRepository


class ColonyService:
    def __init__(
        self, colony_repo: ColonyRepository, hive_repo: HiveRepository
    ) -> None:
        self.colony_repo: ColonyRepository = colony_repo
        self.hive_repo: HiveRepository = hive_repo
        self.invalid_hive_id = "Invalid hive_id"
        self.invalid_colony_id = "Invalid colony_id"

    def _validate_hive_id(self, hive_id: int) -> None:
        if not isinstance(hive_id, int) or hive_id <= 0:
            raise ValueError(self.invalid_hive_id)

    def _validate_colony_id(self, colony_id: int) -> None:
        if not isinstance(colony_id, int) or colony_id <= 0:
            raise ValueError(self.invalid_colony_id)

    def create_colony(self, hive_id: int) -> Colony | None:
        self._validate_hive_id(hive_id)
        if not bool(self.hive_repo.find_by_hive_id(hive_id)):
            raise ValueError(self.invalid_hive_id)
        return self.colony_repo.create(hive_id)
