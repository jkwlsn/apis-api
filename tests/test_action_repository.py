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

    def test_can_find_action_by_valid_action_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "action_id": self.test_action.action_id,
                "notes": self.test_action.notes,
                "inspection_id": self.test_action.inspection_id,
            }
        ]
        repo: ActionRepository = ActionRepository(db=mock_db)

        result: Action | None = repo.find_by_action_id(self.test_action.action_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM actions WHERE action_id = %s LIMIT 1;",
            [self.test_action.action_id],
        )
        assert isinstance(result, Action)
        assert result.action_id == self.test_action.action_id
        assert result.notes == self.test_action.notes
        assert result.inspection_id == self.test_action.inspection_id

    def test_can_not_find_action_by_invalid_action_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ActionRepository = ActionRepository(db=mock_db)

        result: Action | None = repo.find_by_action_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM actions WHERE action_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_can_find_actions_by_valid_inspection_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "action_id": self.test_action.action_id,
                "notes": self.test_action.notes,
                "inspection_id": self.test_action.inspection_id,
            }
        ]
        repo: ActionRepository = ActionRepository(db=mock_db)

        results: list[Action] | None = repo.find_by_inspection_id(
            self.test_action.inspection_id
        )

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM actions WHERE inspection_id = %s;",
            [self.test_action.inspection_id],
        )
        assert isinstance(results, list)
        assert results[0].action_id == self.test_action.action_id

    def test_can_not_find_action_by_invalid_inspection_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = []
        repo: ActionRepository = ActionRepository(db=mock_db)

        result: Action | None = repo.find_by_inspection_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM actions WHERE inspection_id = %s;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "action_id": self.test_action.action_id,
                "notes": self.test_action.notes,
                "inspection_id": self.test_action.inspection_id,
            },
            {
                "action_id": self.test_action_2.action_id,
                "notes": self.test_action_2.notes,
                "inspection_id": self.test_action_2.inspection_id,
            },
            {
                "action_id": self.test_action_3.action_id,
                "notes": self.test_action_3.notes,
                "inspection_id": self.test_action_3.inspection_id,
            },
        ]
        repo: ActionRepository = ActionRepository(db=mock_db)

        results: list[Action] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM actions;", [])
        assert isinstance(results, (list, Action))
        assert results[0].action_id == 1
        assert results[1].action_id == 2
        assert results[2].action_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no apiaries in the db"""
        mock_db.execute.return_value = []
        repo: ActionRepository = ActionRepository(mock_db)

        result: list[Action] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM actions;", [])
        assert result is None

    def test_can_update_valid_action(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "action_id": self.test_action.action_id,
            }
        ]
        repo: ActionRepository = ActionRepository(mock_db)

        result: Action | None = repo.update(
            self.test_action.action_id,
            self.test_action.notes,
            999,
        )

        mock_db.execute.assert_called_once_with(
            "UPDATE actions SET notes = %s, inspection_id = %s RETURNING action_id;",
            [self.test_action.notes, 999, 1],
        )
        assert isinstance(result, Action)
        assert result.action_id == self.test_action.action_id
        assert result.notes == self.test_action.notes
        assert result.inspection_id == 999

    def test_can_not_update_invalid_action(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT UPDATE an invalid action in the database"""
        mock_db.execute.return_value = []
        repo = ActionRepository(mock_db)

        result: list[Action] = repo.update(999, self.test_action.notes, 1)
        mock_db.execute.assert_called_once_with(
            "UPDATE actions SET notes = %s, inspection_id = %s RETURNING action_id;",
            [self.test_action.notes, 1, 999],
        )
        assert result is None
