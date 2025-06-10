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

    def test_can_find_hive_by_valid_hive_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "hive_id": self.test_hive.hive_id,
                "name": self.test_hive.name,
                "apiary_id": self.test_hive.apiary_id,
            }
        ]
        repo: HiveRepository = HiveRepository(db=mock_db)

        result: Hive | None = repo.find_by_hive_id(self.test_hive.hive_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM hives WHERE hive_id = %s LIMIT 1;",
            [self.test_hive.hive_id],
        )
        assert isinstance(result, Hive)
        assert result.hive_id == self.test_hive.hive_id
        assert result.name == self.test_hive.name
        assert result.apiary_id == self.test_hive.apiary_id

    def test_can_not_find_hive_by_invalid_hive_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: HiveRepository = HiveRepository(db=mock_db)

        result: Hive | None = repo.find_by_hive_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM hives WHERE hive_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_can_find_hives_by_valid_apiary_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "hive_id": self.test_hive.hive_id,
                "name": self.test_hive.name,
                "apiary_id": self.test_hive.apiary_id,
            },
            {
                "hive_id": self.test_hive_2.hive_id,
                "name": self.test_hive_2.name,
                "apiary_id": self.test_hive_2.apiary_id,
            },
        ]
        repo: HiveRepository = HiveRepository(db=mock_db)

        result: Hive | None = repo.find_by_apiary_id(self.test_hive.hive_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM hives WHERE apiary_id = %s;",
            [self.test_hive.hive_id],
        )
        assert isinstance(result, list)
        assert result[0].hive_id == self.test_hive.hive_id
        assert result[0].name == self.test_hive.name
        assert result[0].apiary_id == self.test_hive.apiary_id
        assert result[1].hive_id == self.test_hive_2.hive_id
        assert result[1].name == self.test_hive_2.name
        assert result[1].apiary_id == self.test_hive_2.apiary_id

    def test_can_not_find_hive_by_invalid_apiary_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: HiveRepository = HiveRepository(db=mock_db)

        result: Hive | None = repo.find_by_apiary_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM hives WHERE apiary_id = %s;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "hive_id": self.test_hive.hive_id,
                "name": self.test_hive.name,
                "apiary_id": self.test_hive.apiary_id,
            },
            {
                "hive_id": self.test_hive_2.hive_id,
                "name": self.test_hive_2.name,
                "apiary_id": self.test_hive_2.apiary_id,
            },
            {
                "hive_id": self.test_hive_3.hive_id,
                "name": self.test_hive_3.name,
                "apiary_id": self.test_hive_3.apiary_id,
            },
        ]
        repo: HiveRepository = HiveRepository(db=mock_db)

        results: list[Hive] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM hives;", [])
        assert isinstance(results, (list, Hive))
        assert results[0].hive_id == 1
        assert results[1].hive_id == 2
        assert results[2].hive_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no apiaries in the db"""
        mock_db.execute.return_value = []
        repo: HiveRepository = HiveRepository(mock_db)

        result: list[Hive] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM hives;", [])
        assert result is None

    def test_can_update_valid_hive(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "hive_id": self.test_hive.hive_id,
                "name": "UPDATED",
                "apiary_id": self.test_hive.apiary_id,
            }
        ]
        repo: HiveRepository = HiveRepository(mock_db)

        result: list[Hive] = repo.update(1, "UPDATED", 1)

        mock_db.execute.assert_called_once_with(
            "UPDATE hives SET name = %s, apiary_id = %s WHERE hive_id = %s RETURNING hive_id;",
            [
                "UPDATED",
                self.test_hive.apiary_id,
                self.test_hive.hive_id,
            ],
        )
        assert isinstance(result, Hive)
        assert result.hive_id == self.test_hive.hive_id
        assert result.name == "UPDATED"
        assert result.apiary_id == self.test_hive.apiary_id

    def test_can_not_update_invalid_hive(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT UPDATE an invalid hive in the database"""
        mock_db.execute.return_value = []
        repo = HiveRepository(mock_db)

        result = repo.update(1, "BAD UPDATE", 1)
        mock_db.execute.assert_called_once_with(
            "UPDATE hives SET name = %s, apiary_id = %s WHERE hive_id = %s RETURNING hive_id;",
            ["BAD UPDATE", 1, 1],
        )
        assert result is None

    def test_can_delete_valid_hive(self, mock_db: MagicMock) -> None:
        """Respository CAN DELETE a single valid hive in the database"""
        mock_db.execute.return_value = [1]
        repo: HiveRepository = HiveRepository(mock_db)
        result: list[int] = repo.delete(1)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM hives WHERE hive_id = %s RETURNING hive_id;",
            [1],
        )
        assert result is True

    def test_can_not_delete_invalid_hive(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT DELETE an invalid hive in the database"""
        mock_db.execute.return_value = []
        repo: HiveRepository = HiveRepository(mock_db)
        result: list = repo.delete(999)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM hives WHERE hive_id = %s RETURNING hive_id;", [999]
        )
        assert result is False
