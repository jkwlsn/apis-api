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


def test_find_action_by_action_id(
    action_repo: MagicMock, inspection_repo: MagicMock, test_data: Action
) -> None:
    action_id = 1
    action_repo.find_by_action_id.return_value = test_data
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    results: Action | None = action_service.find_action_by_action_id(action_id)

    assert isinstance(results, Action)
    assert results.action_id == test_data.action_id
    assert results.notes == test_data.notes
    assert results.inspection_id == test_data.inspection_id


def test_can_not_find_action_by_missing_action_id(
    action_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    action_id = 999
    action_repo.find_by_action_id.return_value = None
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    result = action_service.find_action_by_action_id(action_id)

    assert result is None


def test_can_not_find_action_by_invalid_action_id(
    action_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    action_id = -1
    action_repo.find_by_action_id.return_value = None
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    with pytest.raises(ValueError, match="Invalid action_id"):
        action_service.find_action_by_action_id(action_id)


def test_find_actions_by_inspection_id(
    action_repo: MagicMock,
    inspection_repo: MagicMock,
    test_data: Action,
    test_data_2: Action,
) -> None:
    action_repo.find_by_inspection_id.return_value = [test_data, test_data_2]
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    results: list[Action] | None = action_service.find_actions_by_inspection_id(1)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], Action)
    assert results[0].inspection_id == test_data.inspection_id
    assert isinstance(results[1], Action)
    assert results[1].inspection_id == test_data_2.inspection_id


def test_can_not_find_action_by_missing_inspection_id(
    action_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    action_repo.find_by_inspection_id.return_value = None
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    results: list[Action] | None = action_service.find_actions_by_inspection_id(999)

    assert results is None


def test_can_not_find_action_by_invalid_inspection_id(
    action_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    action_repo.find_by_inspection_id.return_value = None
    action_service: ActionService = ActionService(action_repo, inspection_repo)

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        action_service.find_actions_by_inspection_id(-1)
