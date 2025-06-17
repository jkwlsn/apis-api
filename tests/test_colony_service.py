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


def test_find_colony_by_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony, test_data_2: Colony
) -> None:
    colony_repo.find_by_hive_id.return_value = [test_data, test_data_2]
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    results: list[Colony] | None = colony_service.find_colony_by_hive_id(1)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], Colony)
    assert results[0].hive_id == test_data.hive_id
    assert isinstance(results[1], Colony)
    assert results[1].hive_id == test_data_2.hive_id


def test_can_not_find_colony_by_missing_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.find_by_hive_id.return_value = None
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    results: list[Colony] | None = colony_service.find_colony_by_hive_id(999)

    assert results is None


def test_can_not_find_colony_by_invalid_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.find_by_hive_id.return_value = None
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid hive_id"):
        colony_service.find_colony_by_hive_id(-1)


def test_update_colony(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.find_by_colony_id.return_value = test_data
    hive_repo.find_by_hive_id.return_value = Hive(1, "Hive 1", 1)
    colony_repo.update.return_value = test_data
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    results: Colony | None = colony_service.update_colony(1, 1)

    assert results.colony_id == test_data.colony_id
    assert results.hive_id == test_data.hive_id


def test_can_not_update_colony_invalid_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.update.return_value = test_data
    colony_id = -1
    hive_id = 1
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        colony_service.update_colony(colony_id, hive_id)


def test_can_not_update_colony_missing_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.find_by_colony_id.return_value = None
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)
    colony_id = 999
    hive_id = 1

    with pytest.raises(ValueError, match="Invalid colony_id"):
        colony_service.update_colony(colony_id, hive_id)


def test_can_not_update_colony_invalid_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.update.return_value = test_data
    colony_id = 1
    hive_id = -1
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid hive_id"):
        colony_service.update_colony(colony_id, hive_id)


def test_can_not_update_colony_missing_hive_id(
    colony_repo: MagicMock, hive_repo: MagicMock, test_data: Colony
) -> None:
    colony_repo.update.return_value = test_data
    hive_repo.find_by_hive_id.return_value = None
    colony_id = 1
    hive_id = 999
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid hive_id"):
        colony_service.update_colony(colony_id, hive_id)


def test_delete_colony(colony_repo: MagicMock, hive_repo: MagicMock) -> None:
    colony_repo.delete.return_value = True
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    result: bool = colony_service.delete_colony(1)

    assert result is True


def test_can_not_delete_colony_missing_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.find_by_colony_id.return_value = None
    colony_repo.delete.return_value = False
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    results: bool = colony_service.delete_colony(999)

    assert results is False


def test_can_not_delete_colony_invalid_colony_id(
    colony_repo: MagicMock, hive_repo: MagicMock
) -> None:
    colony_repo.delete.return_value = False
    colony_repo.find_by_colony_id.return_value = None
    colony_service: ColonyService = ColonyService(colony_repo, hive_repo)

    with pytest.raises(ValueError, match="Invalid colony_id"):
        colony_service.delete_colony(-1)
