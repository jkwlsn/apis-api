"""Test file for Hive service"""

from unittest.mock import MagicMock

import pytest

from models.hive import Hive
from services.hive import HiveService


@pytest.fixture
def hive_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def apiary_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Hive:
    return Hive(hive_id=1, name="Hive 1", apiary_id=1)


@pytest.fixture
def test_data_2() -> Hive:
    return Hive(hive_id=2, name="Hive 2", apiary_id=1)


def test_create_hive(
    hive_repo: MagicMock, apiary_repo: MagicMock, test_data: Hive
) -> None:
    hive_repo.create.return_value = test_data
    name = "Hive 1"
    apiary_id = 1
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    results: Hive | None = hive_service.create_hive(name, apiary_id)

    assert isinstance(results, Hive)
    assert results.hive_id == test_data.hive_id
    assert results.name == name
    assert results.apiary_id == apiary_id


def test_create_hive_missing_name(
    hive_repo: MagicMock, apiary_repo: MagicMock, test_data: Hive
) -> None:
    hive_repo.create.return_value = test_data
    name = "   "
    apiary_id = 1
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    with pytest.raises(ValueError, match="Hive name is required"):
        hive_service.create_hive(name, apiary_id)


def test_can_not_create_hive_invalid_apiary_id(
    hive_repo: MagicMock, apiary_repo: MagicMock, test_data: Hive
) -> None:
    hive_repo.create.return_value = test_data
    name = "Hive 1"
    apiary_id = -1
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    with pytest.raises(ValueError, match="Invalid apiary_id"):
        hive_service.create_hive(name, apiary_id)


def test_can_not_create_hive_missing_apiary_id(
    hive_repo: MagicMock, apiary_repo: MagicMock, test_data: Hive
) -> None:
    hive_repo.create.return_value = test_data
    apiary_repo.find_by_apiary_id.return_value = None
    name = "Hive 1"
    apiary_id = 999
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    with pytest.raises(ValueError, match="Invalid apiary_id"):
        hive_service.create_hive(name, apiary_id)


def test_find_hive_by_hive_id(
    hive_repo: MagicMock, apiary_repo: MagicMock, test_data: Hive
) -> None:
    hive_repo.find_by_hive_id.return_value = test_data
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    results: Hive | None = hive_service.find_hive_by_hive_id(1)

    assert isinstance(results, Hive)
    assert results.hive_id == test_data.hive_id
    assert results.name == test_data.name
    assert results.apiary_id == test_data.apiary_id


def test_can_not_find_hive_by_missing_hive_id(
    hive_repo: MagicMock, apiary_repo: MagicMock
) -> None:
    hive_repo.find_by_hive_id.return_value = None
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    result = hive_service.find_hive_by_hive_id(999)

    assert result is None


def test_can_not_find_hive_by_invalid_hive_id(
    hive_repo: MagicMock, apiary_repo: MagicMock
) -> None:
    hive_repo.find_by_hive_id.return_value = None
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    with pytest.raises(ValueError, match="Invalid hive_id"):
        hive_service.find_hive_by_hive_id(-1)


def test_find_hives_by_apiary_id(
    hive_repo: MagicMock, apiary_repo: MagicMock, test_data: Hive, test_data_2: Hive
) -> None:
    hive_repo.find_by_apiary_id.return_value = [test_data, test_data_2]
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    results: list[Hive] | None = hive_service.find_hives_by_apiary_id(1)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], Hive)
    assert results[0].name == test_data.name
    assert results[0].apiary_id == test_data.apiary_id
    assert isinstance(results[1], Hive)
    assert results[1].name == test_data_2.name
    assert results[1].apiary_id == test_data_2.apiary_id


def test_can_not_find_hives_by_missing_apiary_id(
    hive_repo: MagicMock, apiary_repo: MagicMock
) -> None:
    hive_repo.find_by_apiary_id.return_value = None
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    results: list[Hive] | None = hive_service.find_hives_by_apiary_id(999)

    assert results is None


def test_can_not_find_hives_by_invalid_apiary_id(
    hive_repo: MagicMock, apiary_repo: MagicMock
) -> None:
    hive_repo.find_by_apiary_id.return_value = None
    hive_service: HiveService = HiveService(hive_repo, apiary_repo)

    with pytest.raises(ValueError, match="Invalid apiary_id"):
        hive_service.find_hives_by_apiary_id(-1)
