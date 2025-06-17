"""InspectionService"""

from datetime import datetime

from models.inspection import Inspection
from repositories.colony import ColonyRepository
from repositories.inspection import InspectionRepository


class InspectionService:
    def __init__(
        self, inspection_repo: InspectionRepository, colony_repo: ColonyRepository
    ) -> None:
        self.inspection_repo: InspectionRepository = inspection_repo
        self.colony_repo: ColonyRepository = colony_repo
        self.invalid_colony_id = "Invalid colony_id"
        self.invalid_inspection_id = "Invalid inspection_id"
        self.invalid_inspection_timestamp = "Invalid inspection_timestamp"

    def _validate_inspection_id(self, inspection_id: int) -> None:
        if isinstance(inspection_id, int) is False or inspection_id <= 0:
            raise ValueError(self.invalid_inspection_id)

    def _validate_inspection_timestamp(self, inspection_timestamp: datetime) -> None:
        if isinstance(inspection_timestamp, datetime) is False:
            raise TypeError(self.invalid_inspection_timestamp)

    def _validate_colony_id(self, colony_id: int) -> None:
        if isinstance(colony_id, int) is False or colony_id <= 0:
            raise ValueError(self.invalid_colony_id)

    def _validate_colony_exists(self, colony_id: int) -> None:
        if self.colony_repo.find_by_colony_id(colony_id) is None:
            raise ValueError(self.invalid_colony_id)

    def _validate_inspection_exists(self, inspection_id: int) -> None:
        if self.inspection_repo.find_by_inspection_id(inspection_id) is None:
            raise ValueError(self.invalid_inspection_id)

    def create_inspection(
        self, inspection_timestamp: datetime, colony_id: int
    ) -> Inspection | None:
        self._validate_colony_id(colony_id)
        self._validate_inspection_timestamp(inspection_timestamp=inspection_timestamp)
        self._validate_colony_exists(colony_id)
        return self.inspection_repo.create(
            inspection_timestamp=inspection_timestamp, colony_id=colony_id
        )
