"""Tests for User API Routes"""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app
from schemas.user import UserRead
from services.dependencies import get_user_service
from services.user import UserService

client: TestClient = TestClient(app)


@pytest.fixture
def mock_user_service() -> Generator[MagicMock]:
    mock: MagicMock = MagicMock()
    app.dependency_overrides[get_user_service] = lambda: mock
    return mock


class TestUserRoutes:
    valid_user: UserRead = UserRead(
        user_id=1, username="validuser", password="securepassword123"
    )

    def test_lifespan_coverage(self) -> None:
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 404

    def test_get_user_service_direct(self) -> None:
        service = get_user_service()

        assert service is not None
        assert isinstance(service, UserService)

    def test_can_create_user_with_valid_data(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(return_value=self.valid_user)

        response = client.post(
            "/users",
            json={
                "username": self.valid_user.username,
                "password": self.valid_user.password,
            },
        )

        assert response.status_code == 200
        assert response.json() == self.valid_user.model_dump()
        mock_user_service.create_user.assert_called_once_with(
            username="validuser", password="securepassword123"
        )

    def test_can_not_create_user_with_duplicate_username(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(
            side_effect=ValueError("Username taken")
        )

        response = client.post(
            "/users",
            json={
                "username": "validuser",
                "password": "securepassword123",
            },
        )

        assert response.status_code == 422
        assert response.json()["detail"] == "Username taken"

    def test_can_not_create_user_when_service_returns_none(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(return_value=None)

        response = client.post(
            "/users", json={"username": "validuser", "password": "validpassword123"}
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to create user"
        mock_user_service.create_user.assert_called_once_with(
            username="validuser", password="validpassword123"
        )

    def test_can_not_create_user_with_short_username(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(
            side_effect=ValueError("Username invalid")
        )

        response = client.post(
            "/users",
            json={"username": "ab", "password": "securepassword123"},
        )
        assert response.status_code == 422

    def test_can_not_create_user_with_long_username(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(
            side_effect=ValueError("Username invalid")
        )

        response = client.post(
            "/users",
            json={
                "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 422

    def test_can_not_create_user_with_non_alphanumeric_username(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(
            side_effect=ValueError("Username invalid")
        )

        response = client.post(
            "/users",
            json={"username": "invalid_user!", "password": "securepassword123"},
        )
        assert response.status_code == 422

    def test_can_not_create_user_with_short_password(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.create_user = MagicMock(
            side_effect=ValueError("Username invalid")
        )

        response = client.post(
            "/users",
            json={"username": "validuser", "password": "short"},
        )
        assert response.status_code == 422

    def test_can_find_user_by_valid_username(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.find_user_by_username = MagicMock(
            return_value=self.valid_user
        )

        response = client.get("/users/username/validuser")

        assert response.status_code == 200
        assert response.json() == self.valid_user.model_dump()
        mock_user_service.find_user_by_username.assert_called_once_with(
            username="validuser"
        )

    def test_can_not_find_user_by_invalid_username(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.find_user_by_username = MagicMock(return_value=None)

        response = client.get("/users/username/ghostuser")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_can_find_user_by_valid_user_id(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.find_user_by_user_id = MagicMock(return_value=self.valid_user)

        response = client.get("/users/id/1")

        assert response.status_code == 200
        assert response.json() == self.valid_user.model_dump()
        mock_user_service.find_user_by_user_id.assert_called_once_with(user_id=1)

    def test_can_not_find_user_by_invalid_user_id(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.find_user_by_user_id = MagicMock(return_value=None)

        response = client.get("/users/id/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_can_update_existing_user(self, mock_user_service: UserService) -> None:
        updated_user: UserRead = UserRead(
            user_id=1, username="updateduser", password="newpassword123"
        )
        mock_user_service.update_user = MagicMock(return_value=updated_user)
        mock_user_service.find_user_by_user_id = MagicMock(return_value=updated_user)

        response = client.post(
            "/users/id/1",
            json={"username": "updateduser", "password": "newpassword123"},
        )

        assert response.status_code == 200
        assert response.json() == updated_user.model_dump()
        mock_user_service.update_user.assert_called_once_with(
            user_id=1, username="updateduser", password="newpassword123"
        )

    def test_can_not_update_user_with_invalid_data(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.update_user = MagicMock(
            side_effect=ValueError("Invalid update")
        )

        response = client.post(
            "/users/id/1",
            json={"username": "bad!", "password": "123"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid update"

    def test_can_not_update_nonexistent_user(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.update_user = MagicMock(return_value=None)

        response = client.post(
            "/users/id/999",
            json={"username": "ghostuser", "password": "ghostpassword123"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Update failed: does user exist?"

    def test_can_delete_existing_user(self, mock_user_service: UserService) -> None:
        mock_user_service.delete_user = MagicMock(return_value=True)

        response = client.delete("/users/id/1")

        assert response.status_code == 200
        assert response.json() is True
        mock_user_service.delete_user.assert_called_once_with(user_id=1)

    def test_can_not_delete_nonexistent_user(
        self, mock_user_service: UserService
    ) -> None:
        mock_user_service.delete_user = MagicMock(return_value=False)

        response = client.delete("/users/id/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
