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
