"""Tests for the ApiaryRepository class"""

from unittest.mock import MagicMock

import pytest

from models.apiary import Apiary
from repositories.apiary import ApiaryRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestApiaryRepository:
    test_apiary: Apiary = Apiary(
        apiary_id=1, name="Happy Hives", location="Kent", user_id=1
    )
    test_apiary_2: Apiary = Apiary(
        apiary_id=2, name="Good bees", location="Sussex", user_id=1
    )
    test_apiary_3: Apiary = Apiary(
        apiary_id=3, name="Honey Munchers", location="Wiltshire", user_id=2
    )

    def test_create_apiary(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [{"apiary_id": self.test_apiary.apiary_id}]
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        result: Apiary | None = repo.create(
            self.test_apiary.name, self.test_apiary.location, self.test_apiary.user_id
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO apiaries (name, location, user_id) VALUES (%s, %s, %s) RETURNING apiary_id;",
            [
                self.test_apiary.name,
                self.test_apiary.location,
                self.test_apiary.user_id,
            ],
        )
        assert isinstance(result, Apiary)
        assert result.apiary_id == self.test_apiary.apiary_id
        assert result.name == self.test_apiary.name
        assert result.location == self.test_apiary.location
        assert result.user_id == self.test_apiary.user_id

    def test_create_invalid_apiary(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        result: Apiary | None = repo.create(
            self.test_apiary.name, self.test_apiary.location, self.test_apiary.user_id
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO apiaries (name, location, user_id) VALUES (%s, %s, %s) RETURNING apiary_id;",
            [
                self.test_apiary.name,
                self.test_apiary.location,
                self.test_apiary.user_id,
            ],
        )
        assert result is None

    def test_can_find_apiary_by_valid_apiary_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "apiary_id": self.test_apiary.apiary_id,
                "name": self.test_apiary.name,
                "location": self.test_apiary.location,
                "user_id": self.test_apiary.user_id,
            }
        ]
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        result: Apiary | None = repo.find_by_apiary_id(self.test_apiary.apiary_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM apiaries WHERE apiary_id = %s LIMIT 1;",
            [self.test_apiary.apiary_id],
        )
        assert isinstance(result, Apiary)
        assert result.apiary_id == self.test_apiary.apiary_id
        assert result.name == self.test_apiary.name
        assert result.location == self.test_apiary.location
        assert result.user_id == self.test_apiary.user_id

    def test_can_not_find_apiary_by_invalid_apiary_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        result: Apiary | None = repo.find_by_apiary_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM apiaries WHERE apiary_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_can_find_apiaries_by_valid_user_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "apiary_id": self.test_apiary.apiary_id,
                "name": self.test_apiary.name,
                "location": self.test_apiary.location,
                "user_id": self.test_apiary.user_id,
            },
            {
                "apiary_id": self.test_apiary_2.apiary_id,
                "name": self.test_apiary_2.name,
                "location": self.test_apiary_2.location,
                "user_id": self.test_apiary_2.user_id,
            },
        ]
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        result: Apiary | None = repo.find_by_user_id(self.test_apiary.apiary_id)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM apiaries WHERE user_id = %s;",
            [self.test_apiary.apiary_id],
        )
        assert isinstance(result, list)
        assert result[0].apiary_id == self.test_apiary.apiary_id
        assert result[0].name == self.test_apiary.name
        assert result[0].location == self.test_apiary.location
        assert result[0].user_id == self.test_apiary.user_id
        assert result[1].apiary_id == self.test_apiary_2.apiary_id
        assert result[1].name == self.test_apiary_2.name
        assert result[1].location == self.test_apiary_2.location
        assert result[1].user_id == self.test_apiary_2.user_id

    def test_can_not_find_apiary_by_invalid_user_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        result: Apiary | None = repo.find_by_user_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM apiaries WHERE user_id = %s;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "apiary_id": self.test_apiary.apiary_id,
                "name": self.test_apiary.name,
                "location": self.test_apiary.location,
                "user_id": self.test_apiary.user_id,
            },
            {
                "apiary_id": self.test_apiary_2.apiary_id,
                "name": self.test_apiary_2.name,
                "location": self.test_apiary_2.location,
                "user_id": self.test_apiary_2.user_id,
            },
            {
                "apiary_id": self.test_apiary_3.apiary_id,
                "name": self.test_apiary_3.name,
                "location": self.test_apiary_3.location,
                "user_id": self.test_apiary_3.user_id,
            },
        ]
        repo: ApiaryRepository = ApiaryRepository(db=mock_db)

        results: list[Apiary] = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM apiaries;", [])
        assert isinstance(results, (list, Apiary))
        assert results[0].apiary_id == 1
        assert results[1].apiary_id == 2
        assert results[2].apiary_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no users in the db"""
        mock_db.execute.return_value = []
        repo: ApiaryRepository = ApiaryRepository(mock_db)

        result: list[Apiary] = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM apiaries;", [])
        assert result is None
