"""Test suite for user schema"""

import pytest
from pydantic import ValidationError

from schemas.user import UserCreate, UserRead


class TestUserSchema:
    def test_user_create_valid(self) -> None:
        """Creates a valid user"""
        data = {"username": "test_user", "password": "securepass"}
        user = UserCreate(**data)
        assert user.username == "test_user"
        assert user.password == "securepass"

    def test_user_create_missing_field(self) -> None:
        """Fail as no password provided"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="test_user")
        assert "password" in str(exc_info.value)

    def test_user_read_valid(self) -> None:
        """Reads valid user"""
        data = {"id": 1, "username": "test_user", "password": "securepass"}
        user = UserRead(**data)
        assert user.id == 1
        assert user.username == "test_user"
        assert user.password == "securepass"

    def test_user_read_invalid_id_type(self) -> None:
        """Fails as user id invalid"""
        with pytest.raises(ValidationError) as exc_info:
            UserRead(id="not-an-int", username="test_user", password="securepass")
        assert "id" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main()
