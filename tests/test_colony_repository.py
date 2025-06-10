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
