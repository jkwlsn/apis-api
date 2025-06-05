"""Pytest module for testing the Session class"""

import datetime
import zoneinfo

import pytest

from models.session import Session


@pytest.fixture
def test_session() -> Session:
    return Session(
        1,
        datetime.datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
        ),
        1,
    )


@pytest.fixture
def test_session_2() -> Session:
    return Session(
        1,
        datetime.datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
        ),
        1,
    )


class TestSession:
    def test_session_instance_constructs(self, test_session: Session) -> None:
        """Test session constructs with session_id and user_id."""
        assert test_session.session_id == 1
        assert test_session.session_start == datetime.datetime(
            2020, 6, 23, 2, 10, 25, tzinfo=zoneinfo.ZoneInfo(key="Etc/UTC")
        )
        assert test_session.user_id == 1

    def test_session_instance_pretty_prints(self, test_session: Session) -> None:
        """Test __str__ dunder method pretty prints session instance."""
        assert str(test_session) == "Session(1, 2020-06-23 02:10:25+00:00, 1)"

    def test_session_instances_are_equal(
        self, test_session: Session, test_session_2: Session
    ) -> None:
        """Test __eq__ dunder method is true"""
        assert test_session == test_session_2


if __name__ == "__main__":
    pytest.main()
