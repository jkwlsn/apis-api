"""Pytest module for testing the User class"""

import pytest

from models.user import User


@pytest.fixture
def test_user() -> User:
    return User(1, "test_username", "test_password")


@pytest.fixture
def test_user_2() -> User:
    return User(1, "test_username", "test_password")


class TestUser:
    def test_user_instance_constructs(self, test_user: User) -> None:
        """Test user constructs with user_id, username, and password."""
        assert test_user.user_id == 1
        assert test_user.username == "test_username"
        assert test_user.password == "test_password"

    def test_user_instance_pretty_prints(self, test_user: User) -> None:
        """Test __str__ dunder method pretty prints user instance."""
        assert str(test_user) == "User(1, test_username, test_password)"

    def test_user_instances_are_equal(self, test_user: User, test_user_2: User) -> None:
        """Test __eq__ dunder method is true"""
        assert test_user == test_user_2


if __name__ == "__main__":
    pytest.main()
