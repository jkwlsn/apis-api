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
    location = "  "
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


def test_find_apiary_by_apiary_id(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.find_by_apiary_id.return_value = test_data
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    results: Apiary | None = apiary_service.find_apiary_by_apiary_id(1)

    assert isinstance(results, Apiary)
    assert results.apiary_id == test_data.apiary_id
    assert results.name == test_data.name
    assert results.location == test_data.location
    assert results.user_id == test_data.user_id


def test_can_not_find_apiary_by_apiary_id(
    apiary_repo: MagicMock, user_repo: MagicMock
) -> None:
    apiary_repo.find_by_apiary_id.return_value = None
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    result = apiary_service.find_apiary_by_apiary_id(999)

    assert result is None


def test_find_apiaries_by_user_id(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary, test_data_2: Apiary
) -> None:
    apiary_repo.find_by_user_id.return_value = [test_data, test_data_2]
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    results: list[Apiary] | None = apiary_service.find_apiaries_by_user_id(1)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], Apiary)
    assert results[0].name == test_data.name
    assert results[0].location == test_data.location
    assert results[0].user_id == test_data.user_id
    assert isinstance(results[1], Apiary)
    assert results[1].name == test_data_2.name
    assert results[1].location == test_data_2.location
    assert results[1].user_id == test_data_2.user_id


def test_can_not_find_apiaries_by_user_id(
    apiary_repo: MagicMock, user_repo: MagicMock
) -> None:
    apiary_repo.find_by_user_id.return_value = None
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    results: list[Apiary] | None = apiary_service.find_apiaries_by_user_id(999)

    assert results is None


def test_update_apiary(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.update.return_value = test_data
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    results: Apiary | None = apiary_service.update_apiary(1, "Happy Bees", "Kent", 1)

    assert isinstance(results, Apiary)
    assert results.name == test_data.name
    assert results.location == test_data.location
    assert results.user_id == test_data.user_id


def test_update_apiary_invalid_apiary_id(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.update.return_value = test_data
    apiary_id = -1
    name = "Happy Bees"
    location = "Kent"
    user_id = 1
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Invalid apiary_id"):
        apiary_service.update_apiary(apiary_id, name, location, user_id)


def test_update_apiary_apiary_id_does_not_exist(
    apiary_repo: MagicMock, user_repo: MagicMock
) -> None:
    apiary_repo.find_by_apiary_id.return_value = None
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)
    apiary_id = 999
    name = "Happy Bees"
    location = "Kent"
    user_id = 1

    with pytest.raises(ValueError, match="Invalid apiary_id"):
        apiary_service.update_apiary(apiary_id, name, location, user_id)


def test_update_apiary_invalid_user_id(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.update.return_value = test_data
    apiary_id = 1
    name = "Happy Bees"
    location = "Kent"
    user_id = -1
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Invalid user_id"):
        apiary_service.update_apiary(apiary_id, name, location, user_id)


def test_update_apiary_user_id_does_not_exist(
    apiary_repo: MagicMock, user_repo: MagicMock, test_data: Apiary
) -> None:
    apiary_repo.update.return_value = test_data
    user_repo.find_by_user_id.return_value = None
    apiary_id = 1
    name = "Happy Bees"
    location = "Kent"
    user_id = 999
    apiary_service: ApiaryService = ApiaryService(apiary_repo, user_repo)

    with pytest.raises(ValueError, match="Invalid user_id"):
        apiary_service.update_apiary(apiary_id, name, location, user_id)
