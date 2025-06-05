"""Test suite for session schema"""

import zoneinfo
from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.session import SessionCreate, SessionRead


@pytest.fixture
def test_session_start() -> datetime:
    return datetime(2025, 6, 5, 12, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC"))


class TestSessionSchema:
    def test_session_create_valid(self, test_session_start: datetime) -> None:
        """Creates a valid session"""
        data = {"session_start": test_session_start, "user_id": 1}
        session = SessionCreate(**data)
        assert session.session_start == test_session_start
        assert session.user_id == 1

    def test_session_create_missing_field(self, test_session_start: datetime) -> None:
        """Fail as no user_id provided"""
        with pytest.raises(ValidationError) as exc_info:
            SessionCreate(session_start=test_session_start)
        assert "validation" in str(exc_info.value)

    def test_session_read_valid(self, test_session_start: datetime) -> None:
        """Reads valid session"""
        data = {"session_id": 1, "session_start": test_session_start, "user_id": 1}
        session = SessionRead(**data)
        assert session.session_id == 1
        assert session.session_start == test_session_start
        assert session.user_id == 1

    def test_session_read_invalid_id_type(self, test_session_start: datetime) -> None:
        """Fails as user_id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            SessionRead(
                session_id="not-an-int", session_start=test_session_start, user_id=1
            )
        assert "session_id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
