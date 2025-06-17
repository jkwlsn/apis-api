"""Tests for InspectionService"""

from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from models.colony import Colony
from models.inspection import Inspection
from services.inspection import InspectionService


@pytest.fixture
def inspection_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def colony_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Inspection:
    inspection_timestamp = datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))
    return Inspection(
        inspection_id=1, inspection_timestamp=inspection_timestamp, colony_id=1
    )


@pytest.fixture
def test_data_2() -> Inspection:
    inspection_timestamp = datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))
    return Inspection(
        inspection_id=2, inspection_timestamp=inspection_timestamp, colony_id=2
    )


def test_create_inspection(
    inspection_repo: MagicMock, colony_repo: MagicMock, test_data: Inspection
) -> None:
    inspection_repo.create.return_value = test_data
    inspection_timestamp = datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))
    colony_id = 1
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    results: Inspection | None = inspection_service.create_inspection(
        inspection_timestamp=inspection_timestamp, colony_id=colony_id
    )

    assert isinstance(results, Inspection)
    assert results.inspection_id == test_data.inspection_id
    assert results.inspection_timestamp == test_data.inspection_timestamp
    assert results.colony_id == test_data.colony_id


def test_can_not_create_inspection_invalid_inspection_timestamp(
    inspection_repo: MagicMock, colony_repo: MagicMock
) -> None:
    inspection_timestamp = "2025-06-10"
    colony_id = 1
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    with pytest.raises(TypeError, match="Invalid inspection_timestamp"):
        inspection_service.create_inspection(
            inspection_timestamp=inspection_timestamp,
            colony_id=colony_id,
        )


def test_can_not_create_inspection_invalid_colony_id(
    inspection_repo: MagicMock, colony_repo: MagicMock, test_data: Inspection
) -> None:
    inspection_repo.create.return_value = test_data
    colony_id = -1
    inspection_timestamp = datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    with pytest.raises(ValueError, match="Invalid colony_id"):
        inspection_service.create_inspection(inspection_timestamp, colony_id)


def test_can_not_create_inspection_missing_colony_id(
    inspection_repo: MagicMock, colony_repo: MagicMock, test_data: Inspection
) -> None:
    inspection_repo.create.return_value = test_data
    colony_repo.find_by_colony_id.return_value = None
    inspection_timestamp = datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))
    colony_id = 999
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    with pytest.raises(ValueError, match="Invalid colony_id"):
        inspection_service.create_inspection(inspection_timestamp, colony_id)


def test_find_inspection_by_inspection_id(
    inspection_repo: MagicMock, colony_repo: MagicMock, test_data: Inspection
) -> None:
    inspection_id = 1
    inspection_repo.find_by_inspection_id.return_value = test_data
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    results: Inspection | None = inspection_service.find_inspection_by_inspection_id(
        inspection_id
    )

    assert isinstance(results, Inspection)
    assert results.inspection_id == test_data.inspection_id
    assert results.inspection_timestamp == test_data.inspection_timestamp
    assert results.colony_id == test_data.colony_id


def test_can_not_find_inspection_by_missing_inspection_id(
    inspection_repo: MagicMock, colony_repo: MagicMock
) -> None:
    inspection_id = 999
    inspection_repo.find_by_inspection_id.return_value = None
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    result = inspection_service.find_inspection_by_inspection_id(inspection_id)

    assert result is None


def test_can_not_find_inspection_by_invalid_inspection_id(
    inspection_repo: MagicMock, colony_repo: MagicMock
) -> None:
    inspection_id = -1
    inspection_repo.find_by_inspection_id.return_value = None
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        inspection_service.find_inspection_by_inspection_id(inspection_id)


def test_find_inspections_by_colony_id(
    inspection_repo: MagicMock,
    colony_repo: MagicMock,
    test_data: Inspection,
    test_data_2: Inspection,
) -> None:
    inspection_repo.find_by_colony_id.return_value = [test_data, test_data_2]
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    results: list[Inspection] | None = inspection_service.find_inspections_by_colony_id(
        1
    )

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], Inspection)
    assert results[0].colony_id == test_data.colony_id
    assert isinstance(results[1], Inspection)
    assert results[1].colony_id == test_data_2.colony_id


def test_can_not_find_inspection_by_missing_colony_id(
    inspection_repo: MagicMock, colony_repo: MagicMock
) -> None:
    inspection_repo.find_by_colony_id.return_value = None
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    results: list[Inspection] | None = inspection_service.find_inspections_by_colony_id(
        999
    )

    assert results is None


def test_can_not_find_inspection_by_invalid_colony_id(
    inspection_repo: MagicMock, colony_repo: MagicMock
) -> None:
    inspection_repo.find_by_colony_id.return_value = None
    inspection_service: InspectionService = InspectionService(
        inspection_repo, colony_repo
    )

    with pytest.raises(ValueError, match="Invalid colony_id"):
        inspection_service.find_inspections_by_colony_id(-1)
