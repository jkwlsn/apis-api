"""Tests for SessionRepository class"""

import zoneinfo
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from models.session import Session
from repositories.session import SessionRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_valid_session_data() -> Session:
    return Session(
        1,
        datetime(2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")),
        1,
    )


@pytest.fixture
def test_valid_session_data_2() -> Session:
    return Session(
        1,
        datetime(2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")),
        2,
    )


@pytest.fixture
def test_invalid_session_data() -> Session:
    return Session(2, "Not a Datetime", 2)


class TestSessionRepository:
    def test_create_single_valid_session_passes(
        self, mock_db: MagicMock, test_valid_session_data: Session
    ) -> None:
        """Repository can CREATE a single session in the database"""
        mock_db.execute.return_value = [
            {"session_id": test_valid_session_data.session_id}
        ]
        repo = SessionRepository(mock_db)
        result = repo.create(test_valid_session_data)
        mock_db.execute.assert_called_once_with(
            "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s) RETURNING session_id;",
            [test_valid_session_data.session_start, test_valid_session_data.user_id],
        )
        assert result == [{"session_id": test_valid_session_data.session_id}]

    def test_create_invalid_session_fails(
        self, mock_db: MagicMock, test_invalid_session_data: Session
    ) -> None:
        """Respository can NOT CREATE a single invalid session in the database"""
        mock_db.execute.return_value = []
        repo = SessionRepository(mock_db)
        result = repo.create(test_invalid_session_data)
        mock_db.execute.assert_called_once_with(
            "INSERT INTO sessions (session_start, user_id) VALUES (%s, %s) RETURNING session_id;",
            [
                test_invalid_session_data.session_start,
                test_invalid_session_data.user_id,
            ],
        )
        assert result == []

    def test_find_session_by_valid_session_id_passes(
        self, mock_db: MagicMock, test_valid_session_data: Session
    ) -> None:
        """Respository CAN FIND valid sessions by session_id in the database"""
        mock_db.execute.return_value = [
            {
                "session_id": test_valid_session_data.session_id,
                "session_start": test_valid_session_data.session_start,
                "user_id": test_valid_session_data.user_id,
            }
        ]
        repo = SessionRepository(mock_db)
        result = repo.find_by_session_id(test_valid_session_data.session_id)
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM sessions WHERE session_id = %s;",
            [test_valid_session_data.session_id],
        )
        assert result == [
            {
                "session_id": test_valid_session_data.session_id,
                "session_start": test_valid_session_data.session_start,
                "user_id": test_valid_session_data.user_id,
            }
        ]

    def test_find_session_by_invalid_session_id_fails(
        self, mock_db: MagicMock, test_invalid_session_data: Session
    ) -> None:
        """Respository CAN NOT FIND invalid sessions in the database"""
        mock_db.execute.return_value = []
        repo = SessionRepository(mock_db)
        result = repo.find_by_session_id(test_invalid_session_data.session_id)
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM sessions WHERE session_id = %s;",
            [test_invalid_session_data.session_id],
        )
        assert result == []

    def test_find_session_by_valid_user_id_passes(
        self, mock_db: MagicMock, test_valid_session_data: Session
    ) -> None:
        """Respository CAN FIND valid sessions by user_id in the database"""
        mock_db.execute.return_value = [
            {
                "session_id": test_valid_session_data.session_id,
                "session_start": test_valid_session_data.session_start,
                "user_id": test_valid_session_data.user_id,
            }
        ]
        repo = SessionRepository(mock_db)
        result = repo.find_by_user_id(test_valid_session_data.user_id)
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM sessions WHERE user_id = %s;",
            [test_valid_session_data.user_id],
        )
        assert result == [
            {
                "session_id": test_valid_session_data.session_id,
                "session_start": test_valid_session_data.session_start,
                "user_id": test_valid_session_data.user_id,
            }
        ]

    def test_read_sessions_passes(
        self,
        mock_db: MagicMock,
        test_valid_session_data: Session,
        test_valid_session_data_2: Session,
    ) -> None:
        """Respository CAN READ all valid sessions in the database"""
        mock_db.execute.return_value = [
            {
                "session_id": test_valid_session_data.session_id,
                "session_start": test_valid_session_data.session_start,
                "user_id": test_valid_session_data.user_id,
            },
            {
                "session_id": test_valid_session_data_2.session_id,
                "session_start": test_valid_session_data_2.session_start,
                "user_id": test_valid_session_data_2.user_id,
            },
        ]
        repo = SessionRepository(mock_db)
        result = repo.read()
        mock_db.execute.assert_called_once_with("SELECT * FROM sessions;")
        assert result == [
            {
                "session_id": test_valid_session_data.session_id,
                "session_start": test_valid_session_data.session_start,
                "user_id": test_valid_session_data.user_id,
            },
            {
                "session_id": test_valid_session_data_2.session_id,
                "session_start": test_valid_session_data_2.session_start,
                "user_id": test_valid_session_data_2.user_id,
            },
        ]

    def test_read_empty_sessions_passes(self, mock_db: MagicMock) -> None:
        """Respository CAN READ all valid sessions in the empty database"""
        mock_db.execute.return_value = []
        repo = SessionRepository(mock_db)
        result = repo.read()
        mock_db.execute.assert_called_once_with("SELECT * FROM sessions;")
        assert result == []

    def test_delete_valid_session_passes(
        self, mock_db: MagicMock, test_valid_session_data: Session
    ) -> None:
        """Respository CAN DELETE a single valid session in the database"""
        mock_db.execute.return_value = [test_valid_session_data.session_id]
        repo = SessionRepository(mock_db)
        result = repo.delete(test_valid_session_data.session_id)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM sessions WHERE session_id = %s RETURNING session_id CASCADE;",
            [test_valid_session_data.session_id],
        )
        assert result is True
