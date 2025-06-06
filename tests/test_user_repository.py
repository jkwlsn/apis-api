"""Tests for UserRepository class"""

from unittest.mock import MagicMock

import pytest

from models.user import User
from repositories.user import UserRepository


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_valid_user_data() -> User:
    return User(1, "test_username", "secure_pass")


@pytest.fixture
def test_invalid_user_data() -> User:
    return User(1, "", "secure_pass")


class TestUserRepository:
    def test_create_single_valid_user_passes(
        self, mock_db: MagicMock, test_valid_user_data: User
    ) -> None:
        """Repository can CREATE a single user in the database"""
        mock_db.execute.return_value = [{"user_id": 1}]
        repo = UserRepository(mock_db)
        result = repo.create(test_valid_user_data)
        mock_db.execute.assert_called_once_with(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;",
            ["test_username", "secure_pass"],
        )
        assert result == [{"user_id": 1}]

    def test_create_invalid_user_fails(
        self, mock_db: MagicMock, test_invalid_user_data: User
    ) -> None:
        """Respository can NOT CREATE a single invalid user in the database"""
        mock_db.execute.return_value = []
        repo = UserRepository(mock_db)
        result = repo.create(test_invalid_user_data)
        mock_db.execute.assert_called_once_with(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;",
            ["", "secure_pass"],
        )
        assert result == []

    def test_find_valid_user_passes(self, mock_db: MagicMock) -> None:
        """Respository CAN FIND a single valid user in the database"""
        mock_db.execute.return_value = [
            {"user_id": 1, "username": "test_username", "password": "secure_pass"}
        ]
        repo = UserRepository(mock_db)
        result = repo.find(1)
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM users WHERE user_id = %s;", [1]
        )
        assert result == [
            {"user_id": 1, "username": "test_username", "password": "secure_pass"}
        ]

    def test_find_invalid_user_passes(self, mock_db: MagicMock) -> None:
        """Respository CAN FIND a single invalid user in the database"""
        mock_db.execute.return_value = []
        repo = UserRepository(mock_db)
        result = repo.find(2)
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM users WHERE user_id = %s;", [2]
        )
        assert result == []

    def test_read_users_passes(self, mock_db: MagicMock) -> None:
        """Respository CAN READ all valid users in the database"""
        mock_db.execute.return_value = [
            {"user_id": 1, "username": "test_username", "password": "test_pass"},
            {"user_id": 2, "username": "jake", "password": "secure_pass"},
        ]
        repo = UserRepository(mock_db)
        result = repo.read()
        mock_db.execute.assert_called_once_with("SELECT * FROM users;")
        assert result == [
            {"user_id": 1, "username": "test_username", "password": "test_pass"},
            {"user_id": 2, "username": "jake", "password": "secure_pass"},
        ]

    def test_update_valid_user_passes(self, mock_db: MagicMock) -> None:
        """Respository CAN UPDATE a single valid user in the database"""
        mock_db.execute.return_value = [
            {"user_id": 1, "username": "UPDATED", "password": "secure_pass"}
        ]
        repo = UserRepository(mock_db)
        result = repo.update(1, "UPDATED", "secure_pass")
        mock_db.execute.assert_called_once_with(
            "UPDATE users SET username = %s, password = %s WHERE user_id = %s RETURNING user_id;",
            ["UPDATED", "secure_pass", 1],
        )
        assert result == [
            {"user_id": 1, "username": "UPDATED", "password": "secure_pass"}
        ]

    def test_update_invalid_user_fails(self, mock_db: MagicMock) -> None:
        """Respository CAN NOT UPDATE a single invalid user in the database"""
        mock_db.execute.return_value = [{"user_id": 1}]
        repo = UserRepository(mock_db)
        result = repo.update(2, "BAD UPDATE", "secure_pass")
        mock_db.execute.assert_called_once_with(
            "UPDATE users SET username = %s, password = %s WHERE user_id = %s RETURNING user_id;",
            ["BAD UPDATE", "secure_pass", 2],
        )
        assert result == [{"user_id": 1}]

    def test_delete_valid_user_passes(self, mock_db: MagicMock) -> None:
        """Respository CAN DELETE a single valid user in the database"""
        mock_db.execute.return_value = [1]
        repo = UserRepository(mock_db)
        result = repo.delete(1)
        mock_db.execute.assert_called_once_with(
            "DELETE FROM users WHERE user_id = %s RETURNING user_id;", [1]
        )
        assert result is True
