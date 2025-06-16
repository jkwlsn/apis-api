"""Tests for SessionService class"""

from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from models.session import Session
from models.user import User
from services.session import SessionService


@pytest.fixture
def session_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def user_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_timestamp() -> datetime:
    return datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))


def test_create_session(
    user_repo: MagicMock, session_repo: MagicMock, test_timestamp: datetime
) -> None:
    session_repo.create.return_value = Session(1, test_timestamp, 1)
    user_repo.find_by_user_id.return_value = User(1, "Jake", "hashedpassword")
    session_service = SessionService(session_repo, user_repo)

    results = session_service.create_session(user_id=1)

    session_repo.create.assert_called_once()
    user_repo.find_by_user_id.assert_called_once_with(1)
    assert isinstance(results, Session)
    assert results.session_id == 1
    assert results.user_id == 1


def test_can_not_create_session_invalid_user(
    user_repo: MagicMock, session_repo: MagicMock
) -> None:
    user_repo.find_by_user_id.return_value = None
    session_service = SessionService(session_repo, user_repo)

    with pytest.raises(ValueError, match="User does not exist"):
        session_service.create_session(user_id=1)


def test_find_session_by_session_id(
    user_repo: MagicMock, session_repo: MagicMock, test_timestamp: datetime
) -> None:
    session_repo.find_by_session_id.return_value = Session(1, test_timestamp, 1)
    session_service = SessionService(session_repo, user_repo)

    results = session_service.find_session_by_session_id(1)

    assert results.session_id == 1
    assert results.user_id == 1


def test_can_not_find_session_by_session_id(
    user_repo: MagicMock, session_repo: MagicMock
) -> None:
    session_repo.find_by_session_id.return_value = None
    session_service = SessionService(session_repo, user_repo)

    results = session_service.find_session_by_session_id(999)

    assert results is None


def test_find_session_by_user_id(
    user_repo: MagicMock, session_repo: MagicMock, test_timestamp: datetime
) -> None:
    session_repo.find_by_user_id.return_value = [
        Session(1, test_timestamp, 1),
        Session(2, test_timestamp, 1),
    ]
    session_service = SessionService(session_repo, user_repo)

    results = session_service.find_session_by_user_id(1)

    assert results[0].session_id == 1
    assert results[0].user_id == 1
    assert results[1].session_id == 2
    assert results[1].user_id == 1


def test_can_not_find_session_by_invalid_user_id(
    user_repo: MagicMock, session_repo: MagicMock
) -> None:
    session_repo.find_by_user_id.return_value = None
    session_service = SessionService(session_repo, user_repo)

    results = session_service.find_session_by_user_id(999)

    assert results is None
