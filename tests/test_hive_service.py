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
