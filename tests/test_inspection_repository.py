"""Tests for InspectionRepository class"""

from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from models.inspection import Inspection
from repositories.inspection import InspectionRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


class TestInspectionRepository:
    test_inspection: Inspection = Inspection(
        inspection_id=1,
        inspection_timestamp=datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")
        ),
        colony_id=1,
    )
    test_inspection_2: Inspection = Inspection(
        inspection_id=2,
        inspection_timestamp=datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")
        ),
        colony_id=2,
    )
    test_inspection_3: Inspection = Inspection(
        inspection_id=3,
        inspection_timestamp=datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")
        ),
        colony_id=3,
    )

    def test_create_inspection(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {"inspection_id": self.test_inspection.inspection_id}
        ]
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        result: Inspection | None = repo.create(
            inspection_timestamp=self.test_inspection.inspection_timestamp,
            colony_id=self.test_inspection.colony_id,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO inspections (inspection_timestamp, colony_id) VALUES (%s, %s) RETURNING inspection_id;",
            [
                self.test_inspection.inspection_timestamp,
                self.test_inspection.colony_id,
            ],
        )
        assert isinstance(result, Inspection)
        assert result.inspection_id == self.test_inspection.inspection_id
        assert result.inspection_timestamp == self.test_inspection.inspection_timestamp
        assert result.colony_id == self.test_inspection.colony_id

    def test_create_invalid_inspection(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = []
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        result: Inspection | None = repo.create(
            inspection_timestamp=self.test_inspection.inspection_timestamp,
            colony_id=999,
        )

        mock_db.execute.assert_called_once_with(
            "INSERT INTO inspections (inspection_timestamp, colony_id) VALUES (%s, %s) RETURNING inspection_id;",
            [self.test_inspection.inspection_timestamp, 999],
        )
        assert result is None

    def test_can_find_inspection_by_valid_inspection_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = [
            {
                "inspection_id": self.test_inspection.inspection_id,
                "inspection_timestamp": self.test_inspection.inspection_timestamp,
                "colony_id": self.test_inspection.colony_id,
            }
        ]
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        result: Inspection | None = repo.find_by_inspection_id(
            self.test_inspection.inspection_id
        )

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM inspections WHERE inspection_id = %s LIMIT 1;",
            [self.test_inspection.inspection_id],
        )
        assert isinstance(result, Inspection)
        assert result.inspection_id == self.test_inspection.inspection_id
        assert result.inspection_timestamp == self.test_inspection.inspection_timestamp
        assert result.colony_id == self.test_inspection.colony_id

    def test_can_not_find_inspection_by_invalid_inspection_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = []
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        result: Inspection | None = repo.find_by_inspection_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM inspections WHERE inspection_id = %s LIMIT 1;", [999]
        )
        assert result is None

    def test_can_find_inspections_by_valid_colony_id(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "inspection_id": self.test_inspection.inspection_id,
                "inspection_timestamp": self.test_inspection.inspection_timestamp,
                "colony_id": self.test_inspection.colony_id,
            }
        ]
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        results: list[Inspection] | None = repo.find_by_colony_id(
            self.test_inspection.colony_id
        )

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM inspections WHERE colony_id = %s;",
            [self.test_inspection.colony_id],
        )
        assert isinstance(results, list)
        assert results[0].inspection_id == self.test_inspection.inspection_id

    def test_can_not_find_inspection_by_invalid_colony_id(
        self, mock_db: MagicMock
    ) -> None:
        mock_db.execute.return_value = []
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        result: Inspection | None = repo.find_by_colony_id(999)

        mock_db.execute.assert_called_once_with(
            "SELECT * FROM inspections WHERE colony_id = %s;", [999]
        )
        assert result is None

    def test_read_full_db_returns_all(self, mock_db: MagicMock) -> None:
        mock_db.execute.return_value = [
            {
                "inspection_id": self.test_inspection.inspection_id,
                "inspection_timestamp": self.test_inspection.inspection_timestamp,
                "colony_id": self.test_inspection.colony_id,
            },
            {
                "inspection_id": self.test_inspection_2.inspection_id,
                "inspection_timestamp": self.test_inspection_2.inspection_timestamp,
                "colony_id": self.test_inspection_2.colony_id,
            },
            {
                "inspection_id": self.test_inspection_3.inspection_id,
                "inspection_timestamp": self.test_inspection_3.inspection_timestamp,
                "colony_id": self.test_inspection_3.colony_id,
            },
        ]
        repo: InspectionRepository = InspectionRepository(db=mock_db)

        results: list[Inspection] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM inspections;", [])
        assert isinstance(results, (list, Inspection))
        assert results[0].inspection_id == 1
        assert results[1].inspection_id == 2
        assert results[2].inspection_id == 3

    def test_read_empty_db_returns_none(self, mock_db: MagicMock) -> None:
        """Respository returns None when there are no apiaries in the db"""
        mock_db.execute.return_value = []
        repo: InspectionRepository = InspectionRepository(mock_db)

        result: list[Inspection] | None = repo.read()

        mock_db.execute.assert_called_once_with("SELECT * FROM inspections;", [])
        assert result is None
