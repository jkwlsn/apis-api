"""QueenService"""

from models.queen import Queen
from repositories.colony import ColonyRepository
from repositories.queen import QueenRepository


class QueenService:
    def __init__(
        self, queen_repo: QueenRepository, colony_repo: ColonyRepository
    ) -> None:
        self.queen_repo: QueenRepository = queen_repo
        self.colony_repo: ColonyRepository = colony_repo
        self.invalid_colony_id = "Invalid colony_id"
        self.invalid_queen_id = "Invalid queen_id"

    def _validate_queen_id(self, queen_id: int) -> None:
        if not isinstance(queen_id, int) or queen_id <= 0:
            raise ValueError(self.invalid_queen_id)

    def _validate_colony_id(self, colony_id: int) -> None:
        if not isinstance(colony_id, int) or colony_id <= 0:
            raise ValueError(self.invalid_colony_id)

    def create_queen(
        self, *, colour: str, clipped: bool, colony_id: int
    ) -> Queen | None:
        self._validate_colony_id(colony_id)
        if not bool(self.colony_repo.find_by_colony_id(colony_id)):
            raise ValueError(self.invalid_colony_id)
        return self.queen_repo.create(
            colour=colour, clipped=clipped, colony_id=colony_id
        )

    def find_queen_by_queen_id(self, queen_id: int) -> Queen | None:
        self._validate_queen_id(queen_id)
        return self.queen_repo.find_by_queen_id(queen_id)

    def find_queen_by_colony_id(self, colony_id: int) -> Queen | None:
        self._validate_colony_id(colony_id)
        return self.queen_repo.find_by_colony_id(colony_id)
