"""Tests for the HiveRepository class"""

from unittest.mock import MagicMock

import pytest

from models.hive import Hive
from repositories.hive import HiveRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestHiveRepository:
    test_hive: Hive = Hive(hive_id=1, name="Hive 1", apiary_id=1)
    test_hive_2: Hive = Hive(hive_id=2, name="Hive 2", apiary_id=1)
    test_hive_3: Hive = Hive(hive_id=3, name="Hive 1", apiary_id=2)

    def test_create_hive(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [{"hive_id": self.test_hive.hive_id}]
        repo: HiveRepository = HiveRepository(db=mock_db)

        result: Hive | None = repo.create(self.test_hive.name, self.test_hive.apiary_id)

        mock_db.execute.assert_called_once_with(
            "INSERT INTO hives (name, apiary_id) VALUES (%s, %s) RETURNING hive_id;",
            [
                self.test_hive.name,
                self.test_hive.apiary_id,
            ],
        )
        assert isinstance(result, Hive)
        assert result.hive_id == self.test_hive.hive_id
        assert result.name == self.test_hive.name
        assert result.apiary_id == self.test_hive.apiary_id

    def test_create_invalid_hive(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: HiveRepository = HiveRepository(db=mock_db)

        result: Hive | None = repo.create(self.test_hive.name, 999)

        mock_db.execute.assert_called_once_with(
            "INSERT INTO hives (name, apiary_id) VALUES (%s, %s) RETURNING hive_id;",
            [self.test_hive.name, 999],
        )
        assert result is None
