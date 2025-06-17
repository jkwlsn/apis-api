"""ActionService"""

from models.action import Action
from repositories.action import ActionRepository
from repositories.inspection import InspectionRepository


class ActionService:
    def __init__(
        self, action_repo: ActionRepository, inspection_repo: InspectionRepository
    ) -> None:
        self.action_repo: ActionRepository = action_repo
        self.inspection_repo: InspectionRepository = inspection_repo
        self.invalid_inspection_id = "Invalid inspection_id"
        self.invalid_action_id = "Invalid action_id"
        self.invalid_notes = "Invalid notes"

    def _validate_action_id(self, action_id: int) -> None:
        if isinstance(action_id, int) is False or action_id <= 0:
            raise ValueError(self.invalid_action_id)

    def _validate_notes(self, notes: str) -> None:
        if isinstance(notes, str) is False:
            raise TypeError(self.invalid_notes)

    def _validate_inspection_id(self, inspection_id: int) -> None:
        if isinstance(inspection_id, int) is False or inspection_id <= 0:
            raise ValueError(self.invalid_inspection_id)

    def _validate_inspection_exists(self, inspection_id: int) -> None:
        if self.inspection_repo.find_by_inspection_id(inspection_id) is None:
            raise ValueError(self.invalid_inspection_id)

    def _validate_action_exists(self, action_id: int) -> None:
        if self.action_repo.find_by_action_id(action_id) is None:
            raise ValueError(self.invalid_action_id)

    def create_action(self, notes: str, inspection_id: int) -> Action | None:
        self._validate_inspection_id(inspection_id)
        self._validate_notes(notes=notes)
        self._validate_inspection_exists(inspection_id)
        return self.action_repo.create(notes=notes, inspection_id=inspection_id)

    def find_action_by_action_id(self, action_id: int) -> Action | None:
        self._validate_action_id(action_id)
        return self.action_repo.find_by_action_id(action_id)

    def find_actions_by_inspection_id(self, inspection_id: int) -> list[Action] | None:
        self._validate_inspection_id(inspection_id)
        return self.action_repo.find_by_inspection_id(inspection_id)

    def update_action(
        self, action_id: int, notes: str, inspection_id: int
    ) -> Action | None:
        self._validate_action_id(action_id)
        self._validate_notes(notes=notes)
        self._validate_inspection_id(inspection_id)
        self._validate_action_exists(action_id)
        self._validate_inspection_exists(inspection_id)
        return self.action_repo.update(
            action_id=action_id,
            notes=notes,
            inspection_id=inspection_id,
        )

    def delete_action(self, action_id: int) -> bool:
        self._validate_action_id(action_id)
        return bool(self.action_repo.delete(action_id))
