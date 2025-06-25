"""Tests for UserRepository class"""

from collections.abc import Callable
from unittest.mock import MagicMock

import pytest

from models.user import User
from repositories.user import UserRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


@pytest.fixture
def user_factory() -> Callable[[int, str, str], User]:
    def _factory(user_id: int, username: str, password: str) -> User:
        return User(user_id=user_id, username=username, password=password)

    return _factory


def test_create_valid_user(
    mock_db: MagicMock, user_factory: Callable[[int, str, str], User]
) -> None:
    """Repository can CREATE a single user in the database"""
    test_case: User = user_factory(user_id=1, username="test", password="password")
    mock_db.execute.return_value = [{"user_id": test_case.user_id}]
    repo: UserRepository = UserRepository(db=mock_db)

    result: User | None = repo.create(
        username=test_case.username, password=test_case.password
    )

    mock_db.execute.assert_called_once_with(
        "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;",
        [test_case.username, test_case.password],
    )
    assert isinstance(result, User)
    assert result.user_id == test_case.user_id
    assert result.username == test_case.username
    assert result.password == test_case.password


def test_create_invalid_user_missing_username(mock_db: MagicMock) -> None:
    """Respository can NOT create a user without a username"""
    repo = UserRepository(mock_db)
    result: User | None = repo.create(username="", password="secure_password")
    assert result is None


def test_create_invalid_user_missing_password(mock_db: MagicMock) -> None:
    repo = UserRepository(db=mock_db)
    result: User | None = repo.create(username="username", password="")
    assert result is None


def test_can_find_user_by_user_id(
    mock_db: MagicMock, user_factory: Callable[[int, str, str], User]
) -> None:
    """Respository CAN FIND a single valid user in the database"""
    test_case: User = user_factory(user_id=1, username="test", password="password")
    mock_db.execute.return_value = [
        {
            "user_id": test_case.user_id,
            "username": test_case.username,
            "password": test_case.password,
        }
    ]
    repo: UserRepository = UserRepository(db=mock_db)

    result: User | None = repo.find_by_user_id(user_id=1)

    mock_db.execute.assert_called_once_with(
        "SELECT * FROM users WHERE user_id = %s LIMIT 1;", [1]
    )
    assert isinstance(result, User)
    assert result.user_id == test_case.user_id
    assert result.username == test_case.username
    assert result.password == test_case.password


def test_can_not_find_user_by_user_id(mock_db: MagicMock) -> None:
    """Repository CAN NOT find invalid user"""
    mock_db.execute.return_value = []
    repo: UserRepository = UserRepository(db=mock_db)

    result: User | None = repo.find_by_user_id(user_id=999)

    mock_db.execute.assert_called_once_with(
        "SELECT * FROM users WHERE user_id = %s LIMIT 1;", [999]
    )
    assert result is None


def test_can_find_user_by_username(
    mock_db: MagicMock, user_factory: Callable[[int, str, str], User]
) -> None:
    """Respository CAN FIND a single valid user in the database"""
    test_case: User = user_factory(user_id=1, username="test", password="password")
    mock_db.execute.return_value = [
        {
            "user_id": test_case.user_id,
            "username": test_case.username,
            "password": test_case.password,
        }
    ]
    repo: UserRepository = UserRepository(db=mock_db)

    result: User | None = repo.find_by_username(username="test")

    mock_db.execute.assert_called_once_with(
        "SELECT * FROM users WHERE username = %s LIMIT 1;", [test_case.username]
    )
    assert isinstance(result, User)
    assert result.user_id == test_case.user_id
    assert result.username == test_case.username
    assert result.password == test_case.password


def test_can_not_find_user_by_username(mock_db: MagicMock) -> None:
    """Repository CAN NOT find invalid user"""
    mock_db.execute.return_value = []
    repo: UserRepository = UserRepository(db=mock_db)

    result: User | None = repo.find_by_username(username="BADNAME")

    mock_db.execute.assert_called_once_with(
        "SELECT * FROM users WHERE username = %s LIMIT 1;", ["BADNAME"]
    )
    assert result is None


def test_read_users_returns_all(
    mock_db: MagicMock, user_factory: Callable[[int, str, str], User]
) -> None:
    """Respository returns a list of all users in the DB"""
    test_case: User = user_factory(user_id=1, username="test", password="password")
    test_case_2: User = user_factory(user_id=2, username="test_2", password="password")
    mock_db.execute.return_value = [
        {
            "user_id": test_case.user_id,
            "username": test_case.username,
            "password": test_case.password,
        },
        {
            "user_id": test_case_2.user_id,
            "username": test_case_2.username,
            "password": test_case_2.password,
        },
    ]

    repo = UserRepository(mock_db)
    result = repo.read()

    mock_db.execute.assert_called_once_with("SELECT * FROM users;", [])
    assert result == [test_case, test_case_2]


def test_read_users_returns_none(mock_db: MagicMock) -> None:
    """Respository returns None when there are no users in the db"""
    mock_db.execute.return_value = []
    repo = UserRepository(mock_db)
    result = repo.read()
    mock_db.execute.assert_called_once_with("SELECT * FROM users;", [])
    assert result is None


def test_can_update_valid_user(
    mock_db: MagicMock, user_factory: Callable[[int, str, str], User]
) -> None:
    """Respository CAN UPDATE a single valid user in the database"""
    test_case: User = user_factory(user_id=1, username="test", password="password")
    mock_db.execute.return_value = [
        {"user_id": 1, "username": "UPDATED", "password": "password"}
    ]
    repo = UserRepository(mock_db)

    result = repo.update(1, "UPDATED", "password")

    mock_db.execute.assert_called_once_with(
        "UPDATE users SET username = %s, password = %s WHERE user_id = %s RETURNING user_id;",
        ["UPDATED", "password", 1],
    )
    assert isinstance(result, User)
    assert result.user_id == test_case.user_id
    assert result.username == "UPDATED"
    assert result.password == test_case.password


def test_can_not_update_invalid_user(mock_db: MagicMock) -> None:
    """Respository CAN NOT UPDATE an invalid user in the database"""
    mock_db.execute.return_value = []
    repo = UserRepository(mock_db)
    result = repo.update(999, "BAD UPDATE", "password")
    mock_db.execute.assert_called_once_with(
        "UPDATE users SET username = %s, password = %s WHERE user_id = %s RETURNING user_id;",
        ["BAD UPDATE", "password", 999],
    )
    assert result is None


def test_can_delete_valid_user(mock_db: MagicMock) -> None:
    """Respository CAN DELETE a single valid user in the database"""
    mock_db.execute.return_value = [1]
    repo = UserRepository(mock_db)
    result = repo.delete(1)
    mock_db.execute.assert_called_once_with(
        "DELETE FROM users WHERE user_id = %s RETURNING user_id;", [1]
    )
    assert result is True


def test_can_not_delete_invalid_user(mock_db: MagicMock) -> None:
    """Respository CAN DELETE a single valid user in the database"""
    mock_db.execute.return_value = []
    repo = UserRepository(mock_db)
    result = repo.delete(999)
    mock_db.execute.assert_called_once_with(
        "DELETE FROM users WHERE user_id = %s RETURNING user_id;", [999]
    )
    assert result is False
