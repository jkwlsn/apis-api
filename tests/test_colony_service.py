"""Tests for ColonyService"""

from unittest.mock import MagicMock

import pytest

from models.colony import Colony
from models.hive import Hive
from services.colony import ColonyService


@pytest.fixture
def colony_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def hive_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Colony:
    return Colony(colony_id=1, hive_id=1)


@pytest.fixture
def test_data_2() -> Colony:
    return Colony(colony_id=2, hive_id=2)


def test_create_colony(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.create.return_value = test_data
    hive_id = 1
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    results: Colony | None = colony_service.create_colony(hive_id)

    assert isinstance(results, Colony)
    assert results.colony_id == test_data.colony_id
    assert results.hive_id == hive_id


def test_can_not_create_colony_invalid_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.create.return_value = test_data
    hive_id = -1
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid hive_id"):
        colony_service.create_colony(hive_id)


def test_can_not_create_colony_missing_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.create.return_value = test_data
    hive_repo.find_by_hive_id.return_value = None
    hive_id = 999
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid hive_id"):
        colony_service.create_colony(hive_id)


def test_find_colony_by_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.find_by_colony_id.return_value = test_data
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    results: Colony | None = colony_service.find_colony_by_colony_id(1)

    assert isinstance(results, Colony)
    assert results.colony_id == test_data.colony_id
    assert results.hive_id == test_data.hive_id


def test_can_not_find_colony_by_missing_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.find_by_colony_id.return_value = None
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    result = colony_service.find_colony_by_colony_id(999)

    assert result is None


def test_can_not_find_colony_by_invalid_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.find_by_colony_id.return_value = None
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        colony_service.find_colony_by_colony_id(-1)
