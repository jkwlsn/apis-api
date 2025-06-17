"""HiveService"""

from models.hive import Hive
from repositories.apiary import ApiaryRepository
from repositories.hive import HiveRepository


class HiveService:
    def __init__(
        self, hive_repo: HiveRepository, apiary_repo: ApiaryRepository
    ) -> None:
        self.hive_repo: HiveRepository = hive_repo
        self.apiary_repo: ApiaryRepository = apiary_repo
        self.hive_id_invalid = "Invalid hive_id"
        self.apiary_id_invalid = "Invalid apiary_id"
        self.hive_name_invalid = "Hive name is required"

    def create_hive(self, name: str, apiary_id: int) -> Hive | None:
        if len(name.strip()) <= 0:
            raise ValueError(self.hive_name_invalid)

        if apiary_id <= 0:
            raise ValueError(self.apiary_id_invalid)

        if self.apiary_repo.find_by_apiary_id(apiary_id) is None:
            raise ValueError(self.apiary_id_invalid)

        return self.hive_repo.create(name, apiary_id)

    def find_hive_by_hive_id(self, hive_id: int) -> Hive | None:
        if hive_id <= 0:
            raise ValueError(self.hive_id_invalid)
        return self.hive_repo.find_by_hive_id(hive_id)
