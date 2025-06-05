"""Test suite for inspection schema"""

import zoneinfo
from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.inspection import InspectionCreate, InspectionRead


@pytest.fixture
def test_timestamp() -> datetime:
    return datetime(
        2025, 6, 5, 12, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/London")
    )


class TestInspectionSchema:
    def test_inspection_create_valid(self, test_timestamp: datetime) -> None:
        """Creates a valid inspection"""
        test_data: dict = {"inspection_timestamp": test_timestamp, "colony_id": 1}
        inspection = InspectionCreate(**test_data)
        assert inspection.inspection_timestamp == test_timestamp
        assert inspection.colony_id == 1

    def test_inspection_create_missing_field(self) -> None:
        """Fail as no colony_id provided"""
        with pytest.raises(ValidationError) as exc_info:
            InspectionCreate()
        assert "colony" in str(exc_info.value)

    def test_inspection_read_valid(self, test_timestamp: datetime) -> None:
        """Reads valid inspection"""
        test_data: dict = {
            "inspection_id": 1,
            "inspection_timestamp": test_timestamp,
            "colony_id": 1,
        }
        inspection = InspectionRead(**test_data)
        assert inspection.inspection_id == 1
        assert inspection.inspection_timestamp == test_timestamp
        assert inspection.colony_id == 1

    def test_inspection_read_invalid_id_type(self, test_timestamp: datetime) -> None:
        """Fails as inspection id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            InspectionRead(
                inspection_id="not-an-int",
                inspection_timestamp=test_timestamp,
                colony_id=1,
            )
        assert "inspection_id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
