"""Pytest module for testing the User class"""

import pytest

from lib.user import User


class TestUser:
    def test_user_instance_constructs(pytest) -> None:
        """Test user constructs with user_id, username, and password."""
        user = User(1, "test_username", "test_password")
        assert user.user_id == 1
        assert user.username == "test_username"
        assert user.password == "test_password"

    def test_user_instance_pretty_prints(pytest) -> None:
        """Test __str__ dunder method pretty prints user instance."""
        user = User(1, "test_username", "test_password")
        assert str(user) == "User(1, test_username, test_password)"

    def test_user_instances_are_equal(pytest) -> None:
        """Test __eq__ dunder method is true"""
        user_1 = User(1, "test_username", "test_password")
        user_2 = User(1, "test_username", "test_password")
        assert user_1 == user_2


if __name__ == "__main__":
    pytest.main()
