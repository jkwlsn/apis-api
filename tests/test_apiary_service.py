"""Test file for Apiary service"""

from unittest.mock import MagicMock

import pytest

from models.apiary import Apiary
from services.apiary import ApiaryService


@pytest.fixture
def apiary_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def user_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_data() -> Apiary:
    return Apiary(apiary_id=1, name="Happy Bees", location="Kent", user_id=1)


@pytest.fixture
def test_data_2() -> Apiary:
    return Apiary(apiary_id=2, name="Golden Hives", location="Sussex", user_id=1)


def test_create_apiary(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.create.return_value = test_data
    name = "Happy Bees"
    location = "Kent"
    user_id = 1
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    results: Apiary | None = apiary_service.create_apiary(name, location, user_id)

    assert isinstance(results, Apiary)
    assert results.apiary_id == test_data.apiary_id
    assert results.name == name
    assert results.location == location
    assert results.user_id == user_id


def test_create_apiary_missing_name(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.create.return_value = test_data
    name = "   "
    location = "Kent"
    user_id = 1
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Apiary name is required"):
        apiary_service.create_apiary(name, location, user_id)


def test_create_apiary_missing_location(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.create.return_value = test_data
    name = "Happy Bees"
    location = ""
    user_id = 1
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Location is required"):
        apiary_service.create_apiary(name, location, user_id)


def test_create_apiary_invalid_user_id(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.create.return_value = test_data
    name = "Happy Bees"
    location = "Kent"
    user_id = -1
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Invalid user_id"):
        apiary_service.create_apiary(name, location, user_id)


def test_create_apiary_user_id_does_not_exist(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.create.return_value = test_data
    user_repo.find_by_user_id.return_value = None
    name = "Happy Bees"
    location = "Kent"
    user_id = 999
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Invalid user_id"):
        apiary_service.create_apiary(name, location, user_id)
