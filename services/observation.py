"""ObservationService"""

from models.observation import Observation
from repositories.inspection import InspectionRepository
from repositories.observation import ObservationRepository


class ObservationService:
    def __init__(
        self,
        observation_repo: ObservationRepository,
        inspection_repo: InspectionRepository,
    ) -> None:
        self.observation_repo: ObservationRepository = observation_repo
        self.inspection_repo: InspectionRepository = inspection_repo
        self.invalid_inspection_id = "Invalid inspection_id"
        self.invalid_observation_id = "Invalid observation_id"
        self.invalid_notes = "Invalid notes"

    def _validate_observation_id(self, observation_id: int) -> None:
        if isinstance(observation_id, int) is False or observation_id <= 0:
            raise ValueError(self.invalid_observation_id)

    def _validate_notes(self, notes: str) -> None:
        if isinstance(notes, str) is False:
            raise TypeError(self.invalid_notes)

    def _validate_inspection_id(self, inspection_id: int) -> None:
        if isinstance(inspection_id, int) is False or inspection_id <= 0:
            raise ValueError(self.invalid_inspection_id)

    def _validate_inspection_exists(self, inspection_id: int) -> None:
        if self.inspection_repo.find_by_inspection_id(inspection_id) is None:
            raise ValueError(self.invalid_inspection_id)

    def _validate_observation_exists(self, observation_id: int) -> None:
        if self.observation_repo.find_by_observation_id(observation_id) is None:
            raise ValueError(self.invalid_observation_id)

    def create_observation(
        self,
        *,
        queenright: bool,
        queen_cells: int,
        bias: bool,
        brood_frames: int,
        store_frames: int,
        chalk_brood: bool,
        foul_brood: bool,
        varroa_count: int,
        temper: int,
        notes: str,
        inspection_id: int,
    ) -> Observation | None:
        self._validate_inspection_id(inspection_id)
        self._validate_notes(notes=notes)
        self._validate_inspection_exists(inspection_id)
        return self.observation_repo.create(
            queenright=queenright,
            queen_cells=queen_cells,
            bias=bias,
            brood_frames=brood_frames,
            store_frames=store_frames,
            chalk_brood=chalk_brood,
            foul_brood=foul_brood,
            varroa_count=varroa_count,
            temper=temper,
            notes=notes,
            inspection_id=inspection_id,
        )

    def find_observation_by_observation_id(
        self, observation_id: int
    ) -> Observation | None:
        self._validate_observation_id(observation_id)
        return self.observation_repo.find_by_observation_id(observation_id)
