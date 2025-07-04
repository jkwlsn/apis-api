"""Tests for the Colony Repository"""

from unittest.mock import MagicMock

import pytest

from models.colony import Colony
from repositories.colony import ColonyRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestColonyRepository:
    test_colony: Colony = Colony(colony_id=1, hive_id=1)
    test_colony_2: Colony = Colony(colony_id=2, hive_id=2)
    test_colony_3: Colony = Colony(colony_id=3, hive_id=3)

    def test_create_colony(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [{"colony_id": self.test_colony.colony_id}]
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        result: Colony | None = repo.create(self.test_colony.hive_id)

        mock_db.execute.assert_called_once_with(
            "INSERT INTO colonies (hive_id) VALUES (%s) RETURNING colony_id;",
            [
                self.test_colony.hive_id,
            ],
        )
        assert isinstance(result, Colony)
        assert result.colony_id == self.test_colony.colony_id
        assert result.hive_id == self.test_colony.hive_id

    def test_create_invalid_colony(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        result: Colony | None = repo.create(self.test_colony.hive_id)

        mock_db.execute.assert_called_once_with(
            "INSERT INTO colonies (hive_id) VALUES (%s) RETURNING colony_id;",
            [self.test_colony.hive_id],
        )
        assert result is None

    def test_can_find_colony_by_valid_colony_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "colony_id": self.test_colony.colony_id,
                "hive_id": self.test_colony.hive_id,
            }
        ]
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        result: Colony | None = repo.find_by_colony_id(self.test_colony.colony_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM colonies WHERE colony_id = %s LIMIT 1;",
            [self.test_colony.colony_id],
        )
        assert isinstance(result, Colony)
        assert result.colony_id == self.test_colony.colony_id
        assert result.hive_id == self.test_colony.hive_id

    def test_can_not_find_colony_by_invalid_colony_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        result: Colony | None = repo.find_by_colony_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM colonies WHERE colony_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_can_find_colonies_by_valid_hive_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "colony_id": self.test_colony.colony_id,
                "hive_id": self.test_colony.hive_id,
            }
        ]
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        result: Colony | None = repo.find_by_hive_id(self.test_colony.colony_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM colonies WHERE hive_id = %s LIMIT 1;",
            [self.test_colony.colony_id],
        )
        assert isinstance(result, Colony)
        assert result.colony_id == self.test_colony.colony_id
        assert result.hive_id == self.test_colony.hive_id

    def test_can_not_find_colony_by_invalid_hive_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        result: Colony | None = repo.find_by_hive_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM colonies WHERE hive_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "colony_id": self.test_colony.colony_id,
                "hive_id": self.test_colony.hive_id,
            },
            {
                "colony_id": self.test_colony_2.colony_id,
                "hive_id": self.test_colony_2.hive_id,
            },
            {
                "colony_id": self.test_colony_3.colony_id,
                "hive_id": self.test_colony_3.hive_id,
            },
        ]
        repo: ColonyRepository = ColonyRepository(db=mock_db)

        results: list[Colony] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM colonies;", [])
        assert isinstance(results, (list, Colony))
        assert results[0].colony_id == 1
        assert results[1].colony_id == 2
        assert results[2].colony_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no apiaries in the db"""
        mock_db.execute.return_value = []
        repo: ColonyRepository = ColonyRepository(mock_db)

        result: list[Colony] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM colonies;", [])
        assert result is None

    def test_can_update_valid_colony(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "colony_id": self.test_colony.colony_id,
            }
        ]
        repo: ColonyRepository = ColonyRepository(mock_db)

        result: list[Colony] = repo.update(1, 999)

        mock_db.execute.assert_called_once_with(
            "UPDATE colonies SET hive_id = %s WHERE colony_id = %s RETURNING colony_id;",
            [999, self.test_colony.hive_id],
        )
        assert isinstance(result, Colony)
        assert result.colony_id == self.test_colony.colony_id
        assert result.hive_id == 999

    def test_can_not_update_invalid_colony(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT UPDATE an invalid colony in the database"""
        mock_db.execute.return_value = []
        repo = ColonyRepository(mock_db)

        result = repo.update(1, "BAD UPDATE")
        assert result is None

    def test_can_delete_valid_colony(self, mock_db: MagicMock) -> None:
        """Respository CAN DELETE a single valid colony in the database"""
        mock_db.execute.return_value = [1]
        repo: ColonyRepository = ColonyRepository(mock_db)
        result: list[int] = repo.delete(1)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM colonies WHERE colony_id = %s RETURNING colony_id;",
            [1],
        )
        assert result is True

    def test_can_not_delete_invalid_colony(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT DELETE an invalid colony in the database"""
        mock_db.execute.return_value = []
        repo: ColonyRepository = ColonyRepository(mock_db)
        result: list = repo.delete(999)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM colonies WHERE colony_id = %s RETURNING colony_id;", [999]
        )
        assert result is False
