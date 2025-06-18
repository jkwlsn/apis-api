"""Tests for ObservationService"""

from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from models.inspection import Inspection
from models.observation import Observation
from services.observation import ObservationService


@pytest.fixture
def observation_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def inspection_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Observation:
    return Observation(
        observation_id=1,
        queenright=True,
        queen_cells=5,
        bias=True,
        brood_frames=5,
        store_frames=6,
        chalk_brood=False,
        foul_brood=False,
        varroa_count=10,
        temper=5,
        notes="Example notes",
        inspection_id=1,
    )


def test_create_observation(
    observation_repo: MagicMock, inspection_repo: MagicMock, test_data: Observation
) -> None:
    observation_repo.create.return_value = test_data
    queenright = True
    queen_cells = 5
    bias = True
    brood_frames = 5
    store_frames = 6
    chalk_brood = False
    foul_brood = False
    varroa_count = 10
    temper = 5
    notes = "Example notes"
    inspection_id = 1
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    results: Observation | None = observation_service.create_observation(
        queenright=queenright,
        queen_cells=queen_cells,
        bias=bias,
        brood_frames=brood_frames,
        store_frames=store_frames,
        chalk_brood=chalk_brood,
        foul_brood=foul_brood,
        varroa_count=varroa_count,
        temper=temper,
        notes=notes,
        inspection_id=inspection_id,
    )

    assert isinstance(results, Observation)
    assert results.observation_id == test_data.observation_id
    assert results.notes == test_data.notes
    assert results.inspection_id == test_data.inspection_id


def test_can_not_create_observation_invalid_notes(
    observation_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    queenright = True
    queen_cells = 5
    bias = True
    brood_frames = 5
    store_frames = 6
    chalk_brood = False
    foul_brood = False
    varroa_count = 10
    temper = 5
    notes = 9999999
    inspection_id = 1
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    with pytest.raises(TypeError, match="Invalid notes"):
        observation_service.create_observation(
            queenright=queenright,
            queen_cells=queen_cells,
            bias=bias,
            brood_frames=brood_frames,
            store_frames=store_frames,
            chalk_brood=chalk_brood,
            foul_brood=foul_brood,
            varroa_count=varroa_count,
            temper=temper,
            notes=notes,
            inspection_id=inspection_id,
        )


def test_can_not_create_observation_invalid_inspection_id(
    observation_repo: MagicMock, inspection_repo: MagicMock, test_data: Observation
) -> None:
    observation_repo.create.return_value = test_data
    queenright = True
    queen_cells = 5
    bias = True
    brood_frames = 5
    store_frames = 6
    chalk_brood = False
    foul_brood = False
    varroa_count = 10
    temper = 5
    notes = "Example notes"
    inspection_id = -1
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        observation_service.create_observation(
            queenright=queenright,
            queen_cells=queen_cells,
            bias=bias,
            brood_frames=brood_frames,
            store_frames=store_frames,
            chalk_brood=chalk_brood,
            foul_brood=foul_brood,
            varroa_count=varroa_count,
            temper=temper,
            notes=notes,
            inspection_id=inspection_id,
        )


def test_can_not_create_observation_missing_inspection_id(
    observation_repo: MagicMock, inspection_repo: MagicMock, test_data: Observation
) -> None:
    observation_repo.create.return_value = test_data
    inspection_repo.find_by_inspection_id.return_value = None
    queenright = True
    queen_cells = 5
    bias = True
    brood_frames = 5
    store_frames = 6
    chalk_brood = False
    foul_brood = False
    varroa_count = 10
    temper = 5
    notes = "Example notes"
    inspection_id = 999
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        observation_service.create_observation(
            queenright=queenright,
            queen_cells=queen_cells,
            bias=bias,
            brood_frames=brood_frames,
            store_frames=store_frames,
            chalk_brood=chalk_brood,
            foul_brood=foul_brood,
            varroa_count=varroa_count,
            temper=temper,
            notes=notes,
            inspection_id=inspection_id,
        )


def test_find_observation_by_observation_id(
    observation_repo: MagicMock, inspection_repo: MagicMock, test_data: Observation
) -> None:
    observation_id = 1
    observation_repo.find_by_observation_id.return_value = test_data
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    results: Observation | None = (
        observation_service.find_observation_by_observation_id(observation_id)
    )

    assert isinstance(results, Observation)
    assert results.observation_id == test_data.observation_id
    assert results.notes == test_data.notes
    assert results.inspection_id == test_data.inspection_id


def test_can_not_find_observation_by_missing_observation_id(
    observation_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    observation_id = 999
    observation_repo.find_by_observation_id.return_value = None
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    result = observation_service.find_observation_by_observation_id(observation_id)

    assert result is None


def test_can_not_find_observation_by_invalid_observation_id(
    observation_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    observation_id = -1
    observation_repo.find_by_observation_id.return_value = None
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    with pytest.raises(ValueError, match="Invalid observation_id"):
        observation_service.find_observation_by_observation_id(observation_id)


def test_find_observation_by_inspection_id(
    observation_repo: MagicMock,
    inspection_repo: MagicMock,
    test_data: Observation,
) -> None:
    inspection_id = 1
    observation_repo.find_by_inspection_id.return_value = test_data
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    results: Observation | None = observation_service.find_observation_by_inspection_id(
        inspection_id=inspection_id
    )

    assert results.inspection_id == test_data.inspection_id


def test_can_not_find_observation_by_missing_inspection_id(
    observation_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    inspection_id = 999
    observation_repo.find_by_inspection_id.return_value = None
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    results: Observation | None = observation_service.find_observation_by_inspection_id(
        inspection_id=inspection_id
    )

    assert results is None


def test_can_not_find_observation_by_invalid_inspection_id(
    observation_repo: MagicMock, inspection_repo: MagicMock
) -> None:
    inspection_id = -1
    observation_repo.find_by_inspection_id.return_value = None
    observation_service: ObservationService = ObservationService(
        observation_repo, inspection_repo
    )

    with pytest.raises(ValueError, match="Invalid inspection_id"):
        observation_service.find_observation_by_inspection_id(inspection_id)
