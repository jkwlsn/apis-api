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

    def _validate_hive_id(self, hive_id: int) -> None:
        if not isinstance(hive_id, int) or hive_id <= 0:
            raise ValueError(self.hive_id_invalid)

    def _validate_apiary_id(self, apiary_id: int) -> None:
        if not isinstance(apiary_id, int) or apiary_id <= 0:
            raise ValueError(self.apiary_id_invalid)

    def _validate_name(self, name: str) -> None:
        if not isinstance(name, str) or len(name.strip()) <= 0:
            raise ValueError(self.hive_name_invalid)

    def create_hive(self, name: str, apiary_id: int) -> Hive | None:
        self._validate_apiary_id(apiary_id)

        self._validate_name(name)

        if self.apiary_repo.find_by_apiary_id(apiary_id) is None:
            raise ValueError(self.apiary_id_invalid)

        return self.hive_repo.create(name.strip(), apiary_id)

    def find_hive_by_hive_id(self, hive_id: int) -> Hive | None:
        self._validate_hive_id(hive_id)
        return self.hive_repo.find_by_hive_id(hive_id)

    def find_hives_by_apiary_id(self, apiary_id: int) -> list[Hive] | None:
        self._validate_apiary_id(apiary_id)
        return self.hive_repo.find_by_apiary_id(apiary_id)

    def update_hive(self, hive_id: int, name: str, apiary_id: int) -> Hive | None:
        self._validate_hive_id(hive_id)
        self._validate_apiary_id(apiary_id)
        self._validate_name(name)
        if not bool(self.hive_repo.find_by_hive_id(hive_id=hive_id)):
            raise ValueError(self.hive_id_invalid)
        if not bool(self.apiary_repo.find_by_apiary_id(apiary_id=apiary_id)):
            raise ValueError(self.apiary_id_invalid)
        return self.hive_repo.update(hive_id=hive_id, name=name, apiary_id=apiary_id)

    def delete_hive(self, hive_id: int) -> bool:
        self._validate_hive_id(hive_id)
        return bool(self.hive_repo.delete(hive_id))
