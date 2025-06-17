"""Tests for ActionService"""

from unittest.mock import MagicMock

import pytest

from models.action import Action
from services.action import ActionService


@pytest.fixture
def action_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def inspection_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Action:
    return Action(action_id=1, notes="Example notes", inspection_id=1)


@pytest.fixture
def test_data_2() -> Action:
    return Action(action_id=2, notes="Example notes", inspection_id=2)


def test_create_action(
    action_repo: MagicMock, inspection_repo: MagicMock, test_data: Action
) -> None:
    action_repo.create.return_value = test_data
    notes = "Example note"
    inspection_id = 1
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    results: Action | None = action_service.create_action(
        notes=notes, inspection_id=inspection_id
    )

    assert isinstance(results, Action)
    assert results.action_id == test_data.action_id
    assert results.notes == test_data.notes
    assert results.inspection_id == test_data.inspection_id


def test_can_not_create_action_invalid_notes(
    action_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    notes = 999
    inspection_id = 1
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    with pytest.raises(TypeError, match="Invalid notes"):
        action_service.create_action(
            notes=notes,
            inspection_id=inspection_id,
        )


def test_can_not_create_action_invalid_inspection_id(
    action_repo: MagicMock, inspection_repo: MagicMock, test_data: Action
) -> None:
    action_repo.create.return_value = test_data
    notes = "Example note"
    inspection_id = -1
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        action_service.create_action(notes, inspection_id)


def test_can_not_create_action_missing_inspection_id(
    action_repo: MagicMock, inspection_repo: MagicMock, test_data: Action
) -> None:
    action_repo.create.return_value = test_data
    inspection_repo.find_by_inspection_id.return_value = None
    notes = "Example note"
    inspection_id = 999
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        action_service.create_action(notes, inspection_id)
