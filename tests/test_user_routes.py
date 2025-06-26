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
