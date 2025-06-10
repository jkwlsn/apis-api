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
