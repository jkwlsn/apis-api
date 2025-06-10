"""Tests for SessionRepository class"""

from collections.abc import Callable
from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from models.session import Session
from repositories.session import SessionRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


@pytest.fixture
def session_factory() -> Callable[[int, datetime, int], Session]:
    def _factory(session_id: int, session_start: datetime, user_id: int) -> Session:
        return Session(
            session_id=session_id, session_start=session_start, user_id=user_id
        )

    return _factory


def test_create_single_valid_session_passes(
    mock_db: MagicMock, session_factory: Callable[[int, datetime, int], Session]
) -> None:
    """Repository can CREATE a single session in the database"""
    test_case: Session = session_factory(
        1, datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")), 1
    )
    mock_db.execute.return_value = [{"session_id": 1}]
    repo = SessionRepository(mock_db)
    result = repo.create(test_case.session_start, test_case.user_id)
    mock_db.execute.assert_called_once_with(
        "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s) RETURNING session_id;",
        [test_case.session_start, test_case.user_id],
    )
    assert isinstance(result, Session)
    assert result.session_id == test_case.session_id
    assert result.session_start == test_case.session_start
    assert result.user_id == test_case.user_id


def test_create_invalid_session_fails(mock_db: MagicMock) -> None:
    """Respository can NOT CREATE a single invalid session in the database"""
    mock_db.execute.return_value = []
    repo = SessionRepository(mock_db)
    session_start = datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC"))
    result = repo.create(session_start, 999)
    mock_db.execute.assert_called_once_with(
        "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s) RETURNING session_id;",
        [session_start, 999],
    )
    assert result is None


def test_can_find_session_by_session_id(
    mock_db: MagicMock, session_factory: Callable[[int, datetime, int], Session]
) -> None:
    """Respository CAN FIND valid sessions by session_id in the database"""
    test_case: Session = session_factory(
        1, datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")), 1
    )
    mock_db.execute.return_value = [
        {
            "session_id": test_case.session_id,
            "session_start": test_case.session_start,
            "user_id": test_case.user_id,
        }
    ]
    repo = SessionRepository(mock_db)
    result = repo.find_by_session_id(1)
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM sessions WHERE session_id = %s;", [test_case.session_id]
    )
    assert isinstance(result, list)
    assert result[0].session_id == test_case.session_id
    assert result[0].session_start == test_case.session_start
    assert result[0].user_id == test_case.user_id


def test_can_not_find_session_by_session_id(mock_db: MagicMock) -> None:
    """Respository CAN NOT FIND invalid sessions in the database"""
    mock_db.execute.return_value = []
    repo = SessionRepository(mock_db)
    result = repo.find_by_session_id(999)
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM sessions WHERE session_id = %s;",
        [999],
    )
    assert result is None


def test_can_find_session_by_user_id(
    mock_db: MagicMock, session_factory: Callable[[int, datetime, int], Session]
) -> None:
    """Respository CAN FIND valid sessions by user_id in the database"""
    test_case: Session = session_factory(
        1, datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")), 1
    )
    mock_db.execute.return_value = [
        {
            "session_id": test_case.session_id,
            "session_start": test_case.session_start,
            "user_id": test_case.user_id,
        }
    ]
    repo = SessionRepository(mock_db)
    result = repo.find_by_user_id(test_case.user_id)
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM sessions WHERE user_id = %s;",
        [test_case.user_id],
    )
    assert isinstance(result, list)
    assert result[0].session_id == test_case.session_id
    assert result[0].session_start == test_case.session_start
    assert result[0].user_id == test_case.user_id


def test_can_not_find_session_by_user_id(mock_db: MagicMock) -> None:
    """Respository CAN NOT FIND invalid sessions in the database"""
    mock_db.execute.return_value = []
    repo = SessionRepository(mock_db)
    result = repo.find_by_session_id(999)
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM sessions WHERE session_id = %s;",
        [999],
    )
    assert result is None


def test_read_sessions_returns_all(
    mock_db: MagicMock, session_factory: Callable[[int, datetime, int], Session]
) -> None:
    """Respository CAN READ all valid sessions in the database"""
    test_case: Session = session_factory(
        1,
        datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")),
        1,
    )
    test_case_2: Session = session_factory(
        2,
        datetime(2020, 6, 23, 2, 10, 25, tzinfo=ZoneInfo("Etc/UTC")),
        999,
    )
    mock_db.execute.return_value = [
        {
            "session_id": test_case.session_id,
            "session_start": test_case.session_start,
            "user_id": test_case.user_id,
        },
        {
            "session_id": test_case_2.session_id,
            "session_start": test_case_2.session_start,
            "user_id": test_case_2.user_id,
        },
    ]
    repo = SessionRepository(mock_db)
    results = repo.read()
    mock_db.execute.assert_called_once_with("SELECT * FROM sessions;", [])
    assert results == [test_case, test_case_2]
    assert results[0].session_id == 1
    assert results[0].user_id == 1
    assert results[1].session_id == 2
    assert results[1].user_id == 999


def test_read_no_sessions_returns_none(mock_db: MagicMock) -> None:
    """Respository returns None when there are no users in the db"""
    mock_db.execute.return_value = []
    repo = SessionRepository(mock_db)
    result = repo.read()
    mock_db.execute.assert_called_once_with("SELECT * FROM sessions;", [])
    assert result is None


def test_delete_valid_session_passes(mock_db: MagicMock) -> None:
    """Respository CAN DELETE a single valid session in the database"""
    mock_db.execute.return_value = [1]
    repo = SessionRepository(mock_db)
    result = repo.delete(1)
    mock_db.execute.assert_called_once_with(
        "DELETE FROM sessions WHERE session_id = %s RETURNING session_id;",
        [1],
    )
    assert result is True


def test_can_not_delete_invalid_session(mock_db: MagicMock) -> None:
    """Respository CAN NOT DELETE an invalid session in the database"""
    mock_db.execute.return_value = []
    repo = SessionRepository(mock_db)
    result = repo.delete(999)
    mock_db.execute.assert_called_once_with(
        "DELETE FROM sessions WHERE session_id = %s RETURNING session_id;", [999]
    )
    assert result is False
