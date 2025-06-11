"""Tests for ActionRepository"""

from unittest.mock import MagicMock

import pytest

from models.action import Action
from repositories.action import ActionRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestActionRepository:
    test_action: Action = Action(
        action_id=1,
        notes="Example note",
        inspection_id=1,
    )
    test_action_2: Action = Action(
        action_id=2,
        notes="Example note",
        inspection_id=2,
    )
    test_action_3: Action = Action(
        action_id=3,
        notes="Example note",
        inspection_id=3,
    )

    def test_create_action(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [{"action_id": self.test_action.action_id}]
        repo: ActionRepository = ActionRepository(db=mock_db)

        result: Action | None = repo.create(
            notes=self.test_action.notes,
            inspection_id=self.test_action.inspection_id,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO actions (notes, inspection_id) VALUES (%s, %s) RETURNING action_id;",
            [
                self.test_action.notes,
                self.test_action.inspection_id,
            ],
        )
        assert isinstance(result, Action)
        assert result.action_id == self.test_action.action_id
        assert result.notes == self.test_action.notes
        assert result.inspection_id == self.test_action.inspection_id

    def test_create_invalid_action(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ActionRepository = ActionRepository(db=mock_db)

        result: Action | None = repo.create(
            notes=self.test_action.notes,
            inspection_id=999,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO actions (notes, inspection_id) VALUES (%s, %s) RETURNING action_id;",
            [self.test_action.notes, 999],
        )
        assert result is None
