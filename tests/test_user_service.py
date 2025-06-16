"""Tests for UserService class"""

from unittest.mock import MagicMock

import pytest

from models.user import User
from services.user import UserService


@pytest.fixture
def mock_repo() -> MagicMock:
    return MagicMock()


def test_create_user(mock_repo: MagicMock) -> None:
    username = "Jake"
    password = "Avalidpasswordlongerthanten"
    mock_repo.find_by_username.return_value = None
    mock_repo.create.return_value = User(1, username, password)
    user_service = UserService(mock_repo)

    results = user_service.create_user(username=username, password=password)

    assert isinstance(results, User)
    assert results.username == username
    assert isinstance(results.password, str)


def test_create_user_already_exists(mock_repo: MagicMock) -> None:
    username = "Jake"
    password = "Avalidpasswordlongerthanten"
    mock_repo.find_by_username.return_value = User(1, username, password)
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username already taken"):
        user_service.create_user(username=username, password=password)


def test_create_username_with_invalid_chars(mock_repo: MagicMock) -> None:
    username = "Jake<!£$^'()"
    password = "Avalidpasswordlongerthanten"
    mock_repo.find_by_username.return_value = User(1, username, password)
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username invalid"):
        user_service.create_user(username=username, password=password)


def test_create_username_too_long(mock_repo: MagicMock) -> None:
    username = (
        "Jakesusernameisfartoolongtobeactuallyusefulinfactitwillcauseissuesinthefuture"
    )
    password = "agoodpassword"
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username invalid"):
        user_service.create_user(username=username, password=password)


def test_create_username_too_short(mock_repo: MagicMock) -> None:
    username = "a"
    password = "Agoodpassword"
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username invalid"):
        user_service.create_user(username=username, password=password)


def test_create_username_empty(mock_repo: MagicMock) -> None:
    username = "        "
    password = "Agoodpassword"
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username invalid"):
        user_service.create_user(username=username, password=password)


def test_create_user_password_too_long(mock_repo: MagicMock) -> None:
    username = "Jake"
    password = "Avalidpasswordlongerthantenanddefinitelylongerthanforty"
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Password invalid"):
        user_service.create_user(username=username, password=password)


def test_create_user_password_too_short(mock_repo: MagicMock) -> None:
    username = "Jake"
    password = "short"
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Password invalid"):
        user_service.create_user(username=username, password=password)


def test_create_user_password_empty(mock_repo: MagicMock) -> None:
    username = "Jake"
    password = "        "
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Password invalid"):
        user_service.create_user(username=username, password=password)


def test_find_user_by_user_id(mock_repo: MagicMock) -> None:
    mock_repo.find_by_user_id.return_value = User(1, "Jake", "hashedpassword")
    user_service = UserService(mock_repo)

    results = user_service.find_user_by_user_id(1)

    assert isinstance(results, User)
    assert results.user_id == 1
    assert results.username == "Jake"
    assert results.password == "hashedpassword"


def test_can_not_find_user_by_invalid_user_id(mock_repo: MagicMock) -> None:
    mock_repo.find_by_user_id.return_value = None
    user_service = UserService(mock_repo)

    results = user_service.find_user_by_user_id(999)

    assert results is None


def test_find_user_by_username(mock_repo: MagicMock) -> None:
    mock_repo.find_by_username.return_value = User(1, "jake", "hashedpassword")
    user_service = UserService(mock_repo)

    results = user_service.find_user_by_username("Jake")

    assert isinstance(results, User)
    assert results.user_id == 1
    assert results.username == "jake"
    assert results.password == "hashedpassword"


def test_can_not_find_user_by_invalid_username(mock_repo: MagicMock) -> None:
    mock_repo.find_by_username.return_value = None
    user_service = UserService(mock_repo)

    results = user_service.find_user_by_username("BADUSERNAME")

    assert results is None


def test_update_user(mock_repo: MagicMock) -> None:
    mock_repo.find_by_user_id.return_value = User(1, "jake", "hashedpassword")
    mock_repo.find_by_username.return_value = User(1, "jake", "hashedpassword")
    mock_repo.update.return_value = User(1, "UPDATED", "hashedpassword")
    user_service = UserService(mock_repo)
    results = User(1, "Jake", "hashedpassword")

    results = user_service.update_user(
        user_id=1, username="UPDATED", password="hashedpassword"
    )

    assert results.user_id == 1
    assert results.username == "UPDATED"
    assert results.password == "hashedpassword"


def test_can_not_update_user_with_invalid_user_id(mock_repo: MagicMock) -> None:
    mock_repo.find_by_user_id.return_value = None
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="User does not exist"):
        user_service.update_user(
            user_id=1, username="UPDATED", password="hashedpassword"
        )


def test_can_not_update_user_username_taken(mock_repo: MagicMock) -> None:
    mock_repo.find_by_user_id.return_value = User(1, "jake", "hashedpassword")
    mock_repo.find_by_username.return_value = User(2, "AlreadyTaken", "hashedpassword")
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username already taken"):
        user_service.update_user(
            user_id=1, username="AlreadyTaken", password="hashedpassword"
        )


def test_can_not_update_user_username_invalid(mock_repo: MagicMock) -> None:
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Username invalid"):
        user_service.update_user(
            user_id=1, username="Invalid_Username!!!!!!", password="hashedpassword"
        )


def test_can_not_update_user_password_invalid(mock_repo: MagicMock) -> None:
    user_service = UserService(mock_repo)

    with pytest.raises(ValueError, match="Password invalid"):
        user_service.update_user(user_id=1, username="jake", password="tooshort")


def test_delete_user(mock_repo: MagicMock) -> None:
    mock_repo.delete.return_value = True
    user_service = UserService(mock_repo)

    assert user_service.delete_user(1) is True


def test_can_not_delete_invalid_user(mock_repo: MagicMock) -> None:
    mock_repo.delete.return_value = False
    user_service = UserService(mock_repo)

    assert user_service.delete_user(999) is False
